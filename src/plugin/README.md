# Runelite Wrapped

A runelite plugin that sends event data to the runelite-wrapped api, with the purpose of allowing for the creation of a "Spotify Wrapped" style slide show.

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
