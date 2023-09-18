# Ingestor

This is a FastAPI (HTTP API) that receives POST requests from the runelite wrapped plugin containing event information from the current runelite session, and stores the data in a mongodb instance.

## Overview

Summary of information about this part of the project
* This is an HTTP web service that should receive the telemetry form user's RuneLite RLW plugin
* It currently uses a python HTTP framework called FastAPI
  * FastAPI is a popular modern web framework that allows us to define API endpoints using type hints and Pydantic models (`BaseModel`).
  * Pydantic will handle the JSON de/serialisation
  * The whole service is contained in [this module](src/ingestor/main.py) for now. However we will probably want to centralise the model definitions so that the dagster pipelines can also access them.

## Setup required

You'll need a mongodb instance running somewhere and point to it with the MONGODB_URI env var. I recommend also setting up mongo-express or installing mongo-compass so you can debug/inspect db entries.

To set up the environment variable you can add `MONGODB_URI={your mongo uri}` to the `.env` file in the root of the repository.

## Data Received

At the time of writing these are examples of the data this HTTP API needs to receive:

### Stat changed


```json
{
    "data": {
        "boostedLevel": 99,
        "level": 99,
        "skill": "ATTACK",
        "xp": 21245442
    },
    "event": "stat-changed",
    "timestamp": 1683157906075,
    "username": "jerome-o"
}
```

### GE trade updated

```json
{
    "data": {
        "offer": {
        "ab": 1832350633,
        "ac": 275172041,
        "an": -1381408389,
        "au": 832101099,
        "aw": 430527129,
        "itemId": 5305,
        "price": 5,
        "quantitySold": 1,
        "spent": 5,
        "state": "SOLD",
        "totalQuantity": 1
        },
        "slot": 7
    },
    "event": "grand-exchange-offer-changed",
    "timestamp": 1683157906446,
    "username": "jerome-o"
}
```

### Actor death

TODO: This needs debugging, but it should have an identifier for the actor that died, and the standard `event`, `timestamp`, and `username` fields. With `event` being `"actor-death"`

### Game tick

I suspect this one will be significantly extended over time, but here is the current implementation:

```json
{
    "data": {
        "energy": 10000,
        "health": 99,
        "prayer": 85,
        "sessionTickCount": 380,
        "x": 8128,
        "y": 3008
    },
    "event": "game-tick",
    "timestamp": 1683158133517,
    "username": "jerome-o"
}
```

We will need to do some debugging on the x,y positions - but hopefully that will map directly to a location on the world map.
