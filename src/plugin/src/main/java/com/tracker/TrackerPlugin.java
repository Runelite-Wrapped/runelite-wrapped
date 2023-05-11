package com.tracker;

import com.google.inject.Provides;
import javax.inject.Inject;
import lombok.extern.slf4j.Slf4j;
import net.runelite.api.ChatMessageType;
import net.runelite.api.Client;
import net.runelite.api.GameState;
import net.runelite.api.Player;
import net.runelite.api.Skill;
import net.runelite.api.Actor;
import net.runelite.api.Hitsplat;
import net.runelite.api.coords.LocalPoint;
import net.runelite.api.events.GameStateChanged;
import net.runelite.api.events.StatChanged;
import net.runelite.api.events.HitsplatApplied;
import net.runelite.api.events.GrandExchangeOfferChanged;
import net.runelite.api.events.GameTick;
import net.runelite.api.events.ActorDeath;
import net.runelite.client.config.ConfigManager;
import net.runelite.client.eventbus.Subscribe;
import net.runelite.client.plugins.Plugin;
import net.runelite.client.plugins.PluginDescriptor;

import com.fasterxml.jackson.databind.ObjectMapper;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.RequestBody;
import okhttp3.MediaType;

// import IOException
import java.io.IOException;

// telemetry data class definition
class TelemetryData {
	// timestamp of the event
	private long timestamp;

	// event data
	private Object data;

	// player username
	private String username;

	private String event;

	// constructor
	public TelemetryData(Object data,
			String username, String event) {
		// set timestamp to current time
		timestamp = System.currentTimeMillis();

		// set data to the data passed in
		this.data = data;
		this.username = username;
		this.event = event;
	}

	// getters
	public long getTimestamp() {
		return timestamp;
	}

	public Object getData() {
		return data;
	}

	public String getUsername() {
		return username;
	}

	public String getEvent() {
		return event;
	}
}

// game tick data
class GameTickData {

	// variable definitions
	private int x;
	private int y;
	private int health;
	private int prayer;
	private int energy;
	private int sessionTickCount;

	// constructor
	public GameTickData(int x, int y,
			int health, int prayer,
			int energy, int sessionTickCount) {
		this.x = x;
		this.y = y;
		this.health = health;
		this.prayer = prayer;
		this.energy = energy;
		this.sessionTickCount = sessionTickCount;
	}

	// getters
	public int getX() {
		return x;
	}

	public int getY() {
		return y;
	}

	public int getHealth() {
		return health;
	}

	public int getPrayer() {
		return prayer;
	}

	public int getEnergy() {
		return energy;
	}

	public int getSessionTickCount() {
		return sessionTickCount;
	}
}

class LocationData {
	private int x;
	private int y;

	// constructor
	public LocationData(int x, int y) {
		this.x = x;
		this.y = y;
	}

	// getters
	public int getX() {
		return x;
	}

	public int getY() {
		return y;
	}

	// Static method to create a LocationData object from a LocalPoint object
	public static LocationData fromLocalPoint(
			LocalPoint localPoint) {
		// get x and y coordinates
		int x = localPoint.getX();
		int y = localPoint.getY();

		// return new LocationData object
		return new LocationData(x, y);
	}
}

class ActorData {
	private String name;
	private int combatLevel;
	private LocationData location;

	// constructor
	public ActorData(String name, int combatLevel,
			LocationData location) {
		this.name = name;
		this.combatLevel = combatLevel;
		this.location = location;
	}

	// static method to create an ActorData object from an Actor object
	public static ActorData fromActor(
			Actor actor) {
		// get name and combat level
		String name = actor.getName();
		int combatLevel = actor.getCombatLevel();

		// get location
		LocalPoint localPoint = actor
				.getLocalLocation();
		LocationData location = LocationData
				.fromLocalPoint(localPoint);

		// return new ActorData object
		return new ActorData(name, combatLevel,
				location);
	}

	// getters
	public String getName() {
		return name;
	}

	public int getCombatLevel() {
		return combatLevel;
	}

	public LocationData getLocation() {
		return location;
	}
}

class HitsplatData {
	private Hitsplat hitsplat;
	private ActorData actor;

	// constructor
	public HitsplatData(Hitsplat hitsplat,
			ActorData actor) {
		this.hitsplat = hitsplat;
		this.actor = actor;
	}

	// static method to create a HitsplatData object from a HitsplatApplied event
	public static HitsplatData fromHitsplatApplied(
			HitsplatApplied event) {
		// get hitsplat and actor
		Hitsplat hitsplat = event.getHitsplat();
		Actor actor = event.getActor();
		ActorData actorData = ActorData
				.fromActor(actor);

		// return new HitsplatData object
		return new HitsplatData(hitsplat,
				actorData);
	}

	// getters
	public Hitsplat getHitsplat() {
		return hitsplat;
	}

	public ActorData getActor() {
		return actor;
	}
}

@Slf4j
@PluginDescriptor(name = "Runelite Tracker")
public class TrackerPlugin extends Plugin {

	// private game tick count
	private int tickCount = 0;

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
	public void onGameStateChanged(
			GameStateChanged gameStateChanged) {
		if (gameStateChanged
				.getGameState() == GameState.LOGGED_IN) {
			client.addChatMessage(
					ChatMessageType.GAMEMESSAGE,
					"",
					"Example says "
							+ config.server(),
					null);
		}
	}

	// function that sends telemetry to the server
	// should take in an event object (any type that can be serialised by jackson),
	// and an endpoint
	// will serialise the object, and send it to the server
	private void sendTelemetry(Object event,
			String eventName) {
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
		TelemetryData telemetryData = new TelemetryData(
				event, client.getLocalPlayer()
						.getName(),
				eventName);

		// define and object mapper
		ObjectMapper mapper = new ObjectMapper();

		// get json for the event and handle JsonProcessingException
		try {
			String json = mapper
					.writeValueAsString(
							telemetryData);
			// create a new post request
			Request request = new Request.Builder()
					.url(url)
					.post(RequestBody.create(json,
							MediaType.get(
									"application/json; charset=utf-8")))
					.build();
			log.info("Sending {} to {}",
					json,
					url);

			// send the request and handle IOException
			Response response = okHttpClient
					.newCall(request)
					.execute();
			response.close();

		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	@Subscribe()
	public void onStatChanged(StatChanged event) {
		// send event data to server
		sendTelemetry(event,
				"stat-changed");
	}

	@Subscribe()
	public void onHitsplatApplied(
			HitsplatApplied event) {
		// send event data to server
		sendTelemetry(
				HitsplatData.fromHitsplatApplied(
						event),
				"hitsplat-applied");
	}

	@Subscribe()
	public void onActorDeath(ActorDeath event) {
		// send event data to server
		sendTelemetry(event, "actor-death");
	}

	@Subscribe()
	public void onGrandExchangeOfferChanged(
			GrandExchangeOfferChanged event) {
		// send event data to server
		sendTelemetry(event,
				"grand-exchange-offer-changed");
	}

	@Subscribe()
	public void onGameTick(GameTick event) {
		// increment game tick count
		tickCount++;

		// send event data to server
		// information and send that instead of the event
		sendTelemetry(this.buildGameTickData(),
				"game-tick");

	}

	private GameTickData buildGameTickData() {
		// get player
		Player player = client.getLocalPlayer();

		// get player location
		LocalPoint localPoint = player
				.getLocalLocation();

		// get player location
		int x = localPoint.getX();
		int y = localPoint.getY();

		// get player health
		int health = client.getBoostedSkillLevel(
				Skill.HITPOINTS);

		// get player prayer
		int prayer = client.getBoostedSkillLevel(
				Skill.PRAYER);

		// get player run energy
		int energy = client.getEnergy();

		// create a new game tick data object
		return new GameTickData(
				x, y, health, prayer, energy,
				tickCount);

	}

	@Provides
	TrackerConfig provideConfig(
			ConfigManager configManager) {
		return configManager
				.getConfig(TrackerConfig.class);
	}
}
