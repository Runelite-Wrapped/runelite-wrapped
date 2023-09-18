package com.tracker;

import net.runelite.client.config.Config;
import net.runelite.client.config.ConfigGroup;
import net.runelite.client.config.ConfigItem;

@ConfigGroup("example")
public interface TrackerConfig extends Config {
	@ConfigItem(keyName = "server", name = "Ingress Server", description = "Server to send telemetry to")
	default String server() {
		return "http://localhost:8000/";
	}
}
