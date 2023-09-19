package com.tracker;

import net.runelite.client.RuneLite;
import net.runelite.client.externalplugins.ExternalPluginManager;

public class RuneLiteWrapped {
    public static void main(String[] args)
            throws Exception {
        ExternalPluginManager
                .loadBuiltin(TrackerPlugin.class);
        RuneLite.main(args);
    }
}
