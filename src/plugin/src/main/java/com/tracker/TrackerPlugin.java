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

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonProcessingException;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.MediaType;

// import IOException
import java.io.IOException;

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
							+ config.server(),
					null);
		}
	}

	// function that sends telemetry to the server
	// should take in an event object (any type that can be serialised by jackson),
	// and an endpoint
	// will serialise the object, and send it to the server
	private void sendTelemetry(Object event,
			String endpoint) {
		// define url from config.server() and append endpoint, handle
		// missing trailing slash
		String url = config.server();
		if (!url.endsWith("/")) {
			url += "/";
		}
		url += endpoint;

		// define and object mapper
		ObjectMapper mapper = new ObjectMapper();

		// create a new http client
		OkHttpClient httpClient = new OkHttpClient();

		// get json for the event and handle JsonProcessingException
		try {
			String json = mapper
					.writeValueAsString(event);
			// create a new post request
			Request request = new Request.Builder()
					.url(url)
					.post(RequestBody.create(json,
							MediaType.get(
									"application/json; charset=utf-8")))
					.build();
			log.info("Sending {} to {}", event,
					url);

			// send the request and handle IOException
			try {
				httpClient.newCall(request)
						.execute();
			} catch (IOException e) {
				e.printStackTrace();
				log.info(
						"Failed to send {}",
						event);
				return;
			}
		} catch (JsonProcessingException e) {
			e.printStackTrace();
			return;
		}
	}

	@Subscribe()
	public void onStatChanged(StatChanged event) {
		// send event data to server
		sendTelemetry(event,
				"api/v1/stat-changed");
	}

	@Subscribe()
	public void onHitsplatApplied(
			HitsplatApplied event) {
		// send event data to server
		sendTelemetry(event,
				"api/v1/hitsplat-applied");
	}

	@Subscribe()
	public void onGrandExchangeOfferChanged(
			GrandExchangeOfferChanged event) {
		// send event data to server
		sendTelemetry(event,
				"api/v1/grand-exchange-offer-changed");
	}

	@Subscribe()
	public void onGameTick(GameTick event) {
		// increment game tick count
		tickCount++;

		// only print every 100 ticks
		if (tickCount % tickInterval != 0) {
			return;
		}

		// send event data to server
		// TODO: we should construct and object with important game state
		// information and send that instead of the event
		sendTelemetry(event, "api/v1/game-tick");
	}

	@Provides
	TrackerConfig provideConfig(
			ConfigManager configManager) {
		return configManager
				.getConfig(TrackerConfig.class);
	}
}
