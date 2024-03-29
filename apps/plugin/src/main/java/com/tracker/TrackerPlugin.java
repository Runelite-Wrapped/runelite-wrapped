package com.tracker;

// import IOException
import java.io.IOException;
import javax.inject.Inject;
import java.util.Collection;
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
import net.runelite.api.NPC;
import net.runelite.api.coords.WorldPoint;
import net.runelite.api.events.ActorDeath;
import net.runelite.api.events.GameStateChanged;
import net.runelite.api.events.GameTick;
import net.runelite.api.events.GrandExchangeOfferChanged;
import net.runelite.api.events.HitsplatApplied;
import net.runelite.api.events.StatChanged;
import net.runelite.client.events.PlayerLootReceived;
import net.runelite.client.events.NpcLootReceived;
import net.runelite.client.config.ConfigManager;
import net.runelite.client.eventbus.Subscribe;
import net.runelite.client.plugins.Plugin;
import net.runelite.client.plugins.PluginDescriptor;
import net.runelite.client.game.ItemStack;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import okhttp3.ResponseBody;
import com.tracker.models.TelemetryData;

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
	private final int id;
	// type
	// 0 = unknown
	// 1 = npc
	// 2 = player
	private final int type;

	// static method to create an ActorData object from an Actor object
	public static ActorData fromActor(Actor actor) {
		// get name and combat level
		String name = actor.getName();
		int combatLevel = actor.getCombatLevel();

		// get location
		WorldPoint worldPoint = actor.getWorldLocation();
		LocationData location = LocationData.fromWorldPoint(worldPoint);

		int id = -1;
		int type = 0;

		// check if actor is an NPC
		if (actor instanceof NPC) {
			NPC npc = (NPC) actor;
			id = npc.getId();
			type = 1;
		}

		// check if actor is a player
		if (actor instanceof Player) {
			Player player = (Player) actor;
			id = player.getId();
			type = 2;
		}

		// return new ActorData object
		return new ActorData(name, combatLevel, location, id, type);
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


@Getter
@RequiredArgsConstructor
class ItemStackData {
	private final int id;
	private final int quantity;

	// ignoring local point for now
	// private final LocalPoint location;

	public static ItemStackData fromItemStack(ItemStack itemStack) {
		// get id and quantity
		int id = itemStack.getId();
		int quantity = itemStack.getQuantity();

		// return new ItemStackData object
		return new ItemStackData(id, quantity);
	}
}


// npc loot received data
@Getter
@RequiredArgsConstructor
class LootReceivedData {
	private final ActorData actor;
	private final ItemStackData[] items;

	// static method to create a NpcLootReceivedData object from a NpcLootReceived
	// event
	public static LootReceivedData fromNpcLootReceived(NpcLootReceived event) {
		return fromActorAndStack(event.getNpc(), event.getItems());
	}

	public static LootReceivedData fromPlayerLootReceived(PlayerLootReceived event) {
		return fromActorAndStack(event.getPlayer(), event.getItems());
	}

	private static LootReceivedData fromActorAndStack(Actor actor,
			Collection<ItemStack> itemStack) {
		ActorData npcData = ActorData.fromActor(actor);

		// get items (collection), map them using ItemStackData.fromItemStack, and cast to array
		ItemStackData[] itemStacks =
				itemStack.stream().map(ItemStackData::fromItemStack).toArray(ItemStackData[]::new);

		// return new NpcLootReceivedData object
		return new LootReceivedData(npcData, itemStacks);
	}
}


@Slf4j
@PluginDescriptor(name = "Runelite Tracker")
public class TrackerPlugin extends Plugin {

	// generate random string for session id
	protected static String generateSessionId() {
		return "session-" + System.currentTimeMillis();
	}

	private String sessionId;

	private DbClient dbClient = null;

	@Inject
	private DbClientFactory dbClientFactory;

	@Inject
	private Client client;

	@Inject
	private OkHttpClient okHttpClient;

	@Inject
	private TrackerConfig config;

	// getter and setter for sessionId
	public String getSessionId() {
		if (sessionId == null) {
			sessionId = generateSessionId();
		}
		return sessionId;
	}

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
		if (gameStateChanged.getGameState() == GameState.LOGGING_IN) {
			sessionId = generateSessionId();
		}
	}

	// function that sends telemetry to the server
	// should take in an event object (any type that can be serialised by jackson),
	// and an endpoint
	// will serialise the object, and send it to the server
	private void sendTelemetry(Object event, String eventName) {

		if (this.dbClient == null) {
			this.dbClient = dbClientFactory.createDbClient("rlw.db");
			this.dbClient.initialiseDb();
		}

		// create a new telemetry data object
		TelemetryData telemetryData = new TelemetryData(System.currentTimeMillis(), event,
				client.getLocalPlayer().getName(), eventName, client.getTickCount(),
				getSessionId());

		this.dbClient.StoreTelemetry(telemetryData);
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

	@Subscribe()
	public void onNpcLootReceived(final NpcLootReceived npcLootReceived) {
		// print tick count to console
		log.info("Tick count: {}", client.getTickCount());
		// send event data to server
		sendTelemetry(LootReceivedData.fromNpcLootReceived(npcLootReceived), "loot-received");
	}

	@Subscribe()
	public void onPlayerLootReceived(final PlayerLootReceived playerLootReceived) {
		// print tick count to console
		log.info("Tick count: {}", client.getTickCount());
		// send event data to server
		sendTelemetry(LootReceivedData.fromPlayerLootReceived(playerLootReceived), "loot-received");
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
