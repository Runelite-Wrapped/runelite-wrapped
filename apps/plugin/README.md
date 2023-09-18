# Runelite Wrapped

A runelite plugin that sends event data to the runelite-wrapped api, with the purpose of allowing for the creation of a "Spotify Wrapped" style slide show.

## Overview

Most of the code for this plugin is in the [TrackerPlugin.java](src/plugin/src/main/java/com/tracker/TrackerPlugin.java) file.

A brief list of things this plugin does:
* It subscribes to different game events (i.e. `onGameTick`, `onActorDeath`, `onHitsplatApplied`, etc)
  * These events are defined by RuneLite, and when we "subscribe" to an event, we give the event a function (i.e. event handler) that should be called whenever the event occurs.
* Each of these event handlers build a data object with the information from the event (i.e. `GameTickData`, `ActorData`, `HitsplatData`)
  * These data objects are created by us, and they must align with that the server is expecting
  * Our current server data object definitions can be found [here](src/ingestor/main.py) (link may break in the future)
* The event handler then sends these data objects serialised as JSON via an HTTP post request to the RuneLite Wrapped ingress server.
  * The ingress server address can be configured in the RuneLite app.

## vscode setup

* Install recommended java plugins
* Install jdk (`sudo pacman -S jdk-temurin` for arch linux)
* Configure the debugger setting `java.debug.settings.vmArgs` to be `-ea`
* Add debug config to your `launch.json`:
```json
{
    "type": "java",
    "name": "TrackerPluginTest",
    "request": "launch",
    "mainClass": "com.tracker.TrackerPluginTest",
    "projectName": "tracker"
}
```
