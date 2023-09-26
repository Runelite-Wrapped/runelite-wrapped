import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo import MongoClient

from models.telemetry import (
    ActorDeathEvent,
    GameTickEvent,
    GrandExchangeOfferChangedEvent,
    HitsplatAppliedEvent,
    StatChangedEvent,
    LootReceivedEvent,
)

load_dotenv()

URI = os.environ["MONGO_URI"]

client = MongoClient(URI)
db = client.get_database("runelite-wrapped-raw")
game_tick_collection = db.get_collection("game_ticks")
stat_changed_collection = db.get_collection("stat_changed")
grand_exchange_offer_changed_collection = db.get_collection(
    "grand_exchange_offer_changed"
)
hitsplat_applied_collection = db.get_collection("hitsplat_applied")
actor_death_collection = db.get_collection("actor_death")
loot_received_collection = db.get_collection("loot_received")

app = FastAPI()


@app.post("/api/v1/event/game-tick/")
async def game_tick(event: GameTickEvent):
    game_tick_collection.insert_one(event.dict())
    return {"message": "OK"}


@app.post("/api/v1/event/stat-changed/")
async def stat_change(event: StatChangedEvent):
    stat_changed_collection.insert_one(event.dict())
    return {"message": "OK"}


@app.post("/api/v1/event/grand-exchange-offer-changed/")
async def grand_exchange_offer_change(event: GrandExchangeOfferChangedEvent):
    grand_exchange_offer_changed_collection.insert_one(event.dict())
    return {"message": "OK"}


@app.post("/api/v1/event/hitsplat-applied/")
async def hitsplat_applied(event: HitsplatAppliedEvent):
    hitsplat_applied_collection.insert_one(event.dict())
    return {"message": "OK"}


@app.post("/api/v1/event/actor-death/")
async def actor_death(event: ActorDeathEvent):
    actor_death_collection.insert_one(event.dict())
    return {"message": "OK"}


@app.post("/api/v1/event/loot-received/")
async def loot_received(event: LootReceivedEvent):
    loot_received_collection.insert_one(event.dict())
    return {"message": "OK"}


def main():
    from uvicorn import run

    run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
