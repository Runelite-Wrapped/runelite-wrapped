./gradlew clean shadowJar
scp build/libs/tracker.jar rlw:~/srv/runelitewrapped.jar
scp jankdeploy/runelitewrapped.bat rlw:~/srv/
