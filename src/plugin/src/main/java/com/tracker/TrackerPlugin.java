package com.tracker;

// import IOException
import java.io.IOException;
import javax.inject.Inject;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.inject.Provides;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import net.runelite.api.Actor;
import net.runelite.api.ChatMessageType;
import net.runelite.api.Client;
import net.runelite.api.GameState;
import net.runelite.api.Hitsplat;
import net.runelite.api.Player;
import net.runelite.api.Skill;
import net.runelite.api.coords.WorldPoint;
import net.runelite.api.events.ActorDeath;
import net.runelite.api.events.GameStateChanged;
import net.runelite.api.events.GameTick;
import net.runelite.api.events.GrandExchangeOfferChanged;
import net.runelite.api.events.HitsplatApplied;
import net.runelite.api.events.StatChanged;
import net.runelite.client.config.ConfigManager;
import net.runelite.client.eventbus.Subscribe;
import net.runelite.client.plugins.Plugin;
import net.runelite.client.plugins.PluginDescriptor;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import okhttp3.ResponseBody;

// telemetry data class definition
@Getter
@RequiredArgsConstructor
class TelemetryData {
	private final long timestamp;
	private final Object data;
	private final String username;
	private final String event;
	private final long tickCount;
}


// game tick data
@Getter
@RequiredArgsConstructor
class GameTickData {
	private final int health;
	private final int prayer;
	private final int energy;
	private final int sessionTickCount;
	private final int[] equipmentIds;
	private final LocationData location;
}


@Getter
@RequiredArgsConstructor
class LocationData {
	private final int x;
	private final int y;
	private final int regionId;

	// Static method to create a LocationData object from a LocalPoint object
	public static LocationData fromWorldPoint(WorldPoint worldPoint) {
		// get x and y coordinates
		int x = worldPoint.getX();
		int y = worldPoint.getY();
		int regionId = worldPoint.getRegionID();

		// return new LocationData object
		return new LocationData(x, y, regionId);
	}
}


@Getter
@RequiredArgsConstructor
class ActorData {
	private final String name;
	private final int combatLevel;
	private final LocationData location;

	// static method to create an ActorData object from an Actor object
	public static ActorData fromActor(Actor actor) {
		// get name and combat level
		String name = actor.getName();
		int combatLevel = actor.getCombatLevel();

		// get location
		WorldPoint worldPoint = actor.getWorldLocation();
		LocationData location = LocationData.fromWorldPoint(worldPoint);

		// return new ActorData object
		return new ActorData(name, combatLevel, location);
	}
}


@Getter
@RequiredArgsConstructor
class HitsplatData {
	private final Hitsplat hitsplat;
	private final ActorData actor;

	// static method to create a HitsplatData object from a HitsplatApplied event
	public static HitsplatData fromHitsplatApplied(HitsplatApplied event) {
		// get hitsplat and actor
		Hitsplat hitsplat = event.getHitsplat();
		Actor actor = event.getActor();
		ActorData actorData = ActorData.fromActor(actor);

		// return new HitsplatData object
		return new HitsplatData(hitsplat, actorData);
	}
}


@Slf4j
@PluginDescriptor(name = "Runelite Tracker")
public class TrackerPlugin extends Plugin {

	@Inject
	private Client client;

	@Inject
	private OkHttpClient okHttpClient;

	@Inject
	private TrackerConfig config;

	@Override
	protected void startUp() throws Exception {
		log.info("Example started!");

	}

	@Override
	protected void shutDown() throws Exception {
		log.info("Example stopped!");
	}

	@Subscribe
	public void onGameStateChanged(GameStateChanged gameStateChanged) {
		if (gameStateChanged.getGameState() == GameState.LOGGED_IN) {
			client.addChatMessage(ChatMessageType.GAMEMESSAGE, "",
					"Example says " + config.server(), null);
		}
	}

	// function that sends telemetry to the server
	// should take in an event object (any type that can be serialised by jackson),
	// and an endpoint
	// will serialise the object, and send it to the server
	private void sendTelemetry(Object event, String eventName) {
		// define url from config.server() and append endpoint, handle
		// missing trailing slash, and add "api/v1/event"
		String url = config.server();
		if (!url.endsWith("/")) {
			url += "/";
		}
		url += "api/v1/event";
		// add event name to url
		url += "/" + eventName + "/";

		// create a new telemetry data object
		TelemetryData telemetryData = new TelemetryData(System.currentTimeMillis(), event,
				client.getLocalPlayer().getName(), eventName);

		// define and object mapper
		ObjectMapper mapper = new ObjectMapper();

		// get json for the event and handle JsonProcessingException
		try {
			String json = mapper.writeValueAsString(telemetryData);
			// create a new post request
			Request request = new Request.Builder().url(url).post(
					RequestBody.create(json, MediaType.get("application/json; charset=utf-8")))
					.build();
			log.info("Sending {} to {}", json, url);

			// send the request and handle IOException
			okHttpClient.newCall(request).enqueue(new Callback() {
				@Override
				public void onFailure(Call call, IOException e) {
					e.printStackTrace();
				}

				@Override
				public void onResponse(Call call, Response response) throws IOException {
					try (ResponseBody responseBody = response.body()) {
						if (!response.isSuccessful())
							throw new IOException("Unexpected code " + response);
						System.out.println(responseBody.string());
					}
				}
			});

		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	@Subscribe()
	public void onStatChanged(StatChanged event) {

		// print tick count to console
		log.info("Tick count: {}", client.getTickCount());
		// send event data to server
		sendTelemetry(event, "stat-changed");
	}

	@Subscribe()
	public void onHitsplatApplied(HitsplatApplied event) {
		// print tick count to console
		log.info("Tick count: {}", client.getTickCount());
		// send event data to server
		sendTelemetry(HitsplatData.fromHitsplatApplied(event), "hitsplat-applied");
	}

	@Subscribe()
	public void onActorDeath(ActorDeath event) {
		// print tick count to console
		log.info("Tick count: {}", client.getTickCount());
		// send event data to server
		sendTelemetry(ActorData.fromActor(event.getActor()), "actor-death");
	}

	@Subscribe()
	public void onGrandExchangeOfferChanged(GrandExchangeOfferChanged event) {
		// print tick count to console
		log.info("Tick count: {}", client.getTickCount());

		// TODO(j.swannack): the first time this fires after a user signs in, the local
		// player is null and that causes errors (when trying to get the name), this
		// should be fixed somehow.

		// send event data to server
		sendTelemetry(event, "grand-exchange-offer-changed");
	}

	@Subscribe()
	public void onGameTick(GameTick event) {

		// print tick count to console
		log.info("Tick count: {}", client.getTickCount());

		// send event data to server
		// information and send that instead of the event
		sendTelemetry(this.buildGameTickData(), "game-tick");

	}

	private GameTickData buildGameTickData() {
		// get player
		Player player = client.getLocalPlayer();

		int[] equipmentIds = player.getPlayerComposition().getEquipmentIds();

		// get player location
		WorldPoint localPoint = player.getWorldLocation();
		LocationData location = LocationData.fromWorldPoint(localPoint);

		// get player health
		int health = client.getBoostedSkillLevel(Skill.HITPOINTS);

		// get player prayer
		int prayer = client.getBoostedSkillLevel(Skill.PRAYER);

		// get player run energy
		int energy = client.getEnergy();

		// create a new game tick data object
		return new GameTickData(health, prayer, energy, client.getTickCount(), equipmentIds,
				location);

	}

	@Provides
	TrackerConfig provideConfig(ConfigManager configManager) {
		return configManager.getConfig(TrackerConfig.class);
	}
}
