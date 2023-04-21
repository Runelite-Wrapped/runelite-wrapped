package com.example;

import net.runelite.client.RuneLite;
import net.runelite.client.externalplugins.ExternalPluginManager;

public class TrackerPluginTest {
	public static void main(String[] args)
			throws Exception {
		ExternalPluginManager
				.loadBuiltin(TrackerPlugin.class);
		RuneLite.main(args);
	}
}
