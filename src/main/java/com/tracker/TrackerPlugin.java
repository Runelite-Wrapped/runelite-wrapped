package com.tracker;

import com.google.inject.Provides;
import javax.inject.Inject;
import lombok.extern.slf4j.Slf4j;
import net.runelite.api.ChatMessageType;
import net.runelite.api.Client;
import net.runelite.api.GameState;
import net.runelite.api.events.GameStateChanged;
import net.runelite.api.events.StatChanged;
import net.runelite.api.events.HitsplatApplied;
import net.runelite.api.events.GrandExchangeOfferChanged;
import net.runelite.api.events.GameTick;
import net.runelite.client.config.ConfigManager;
import net.runelite.client.eventbus.Subscribe;
import net.runelite.client.plugins.Plugin;
import net.runelite.client.plugins.PluginDescriptor;

@Slf4j
@PluginDescriptor(name = "Runelite Tracker")
public class TrackerPlugin extends Plugin {

	// private game tick count
	private int tickCount = 0;
	private int tickInterval = 10;

	@Inject
	private Client client;

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
							+ config.greeting(),
					null);
		}
	}

	@Subscribe()
	public void onStatChanged(StatChanged event) {
		log.info("StatChanged: {}", event);
		client.addChatMessage(
				ChatMessageType.GAMEMESSAGE,
				"",
				"StatChanged: " + event,
				null);
	}

	@Subscribe()
	public void onHitsplatApplied(
			HitsplatApplied event) {
		log.info("HitsplatApplied: {}", event);
		client.addChatMessage(
				ChatMessageType.GAMEMESSAGE,
				"",
				"HitsplatApplied: " + event,
				null);
	}

	@Subscribe()
	public void onGrandExchangeOfferChanged(
			GrandExchangeOfferChanged event) {
		log.info("GrandExchangeOfferChanged: {}",
				event);
		client.addChatMessage(
				ChatMessageType.GAMEMESSAGE,
				"",
				"GrandExchangeOfferChanged: "
						+ event,
				null);
	}

	@Subscribe()
	public void onGameTick(GameTick event) {
		log.info("GameTick: {}", event);

		// increment game tick count
		tickCount++;

		// only print every 100 ticks
		if (tickCount % tickInterval != 0) {
			return;
		}

		client.addChatMessage(
				ChatMessageType.GAMEMESSAGE,
				"",
				"GameTick: " + event,
				null);
	}

	@Provides
	TrackerConfig provideConfig(
			ConfigManager configManager) {
		return configManager
				.getConfig(TrackerConfig.class);
	}
}
