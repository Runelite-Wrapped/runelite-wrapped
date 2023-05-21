import os
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

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

app = FastAPI()


class LocationData(BaseModel):
    x: int
    y: int
    regionId: int


class ActorData(BaseModel):
    combatLevel: int
    location: LocationData
    name: str

class GameTickData(BaseModel):
    energy: int
    health: int
    prayer: int
    sessionTickCount: int
    location: LocationData
    equipmentIds: Optional[List[int]] = None


class StatChangedData(BaseModel):
    boostedLevel: int
    level: int
    skill: str
    xp: int


class OfferData(BaseModel):
    ab: int
    ac: int
    an: int
    au: int
    aw: int
    itemId: int
    price: int
    quantitySold: int
    spent: int
    state: str
    totalQuantity: int


class GrandExchangeOfferData(BaseModel):
    offer: OfferData
    slot: int


class HitsplatData(BaseModel):
    amount: int
    disappearsOnGameCycle: int
    hitsplatType: int
    mine: bool
    others: bool


class HitsplatAppliedData(BaseModel):
    actor: ActorData
    hitsplat: HitsplatData


class ActorDeathData(BaseModel):
    combatLevel: int
    location: LocationData
    name: str


class GameEventBase(BaseModel):
    event: str
    timestamp: int
    username: str


class GameTickEvent(GameEventBase):
    data: GameTickData


class StatChangedEvent(GameEventBase):
    data: StatChangedData


class GrandExchangeOfferChangedEvent(GameEventBase):
    data: GrandExchangeOfferData


class HitsplatAppliedEvent(GameEventBase):
    data: HitsplatAppliedData


class ActorDeathEvent(GameEventBase):
    data: ActorDeathData


@app.post("/api/v1/event/game-tick/")
async def game_tick(event: GameTickEvent):
    game_tick_collection.insert_one(event.dict())
    return {"message": "OK"}


@app.post("/api/v1/event/stat-changed")
async def stat_change(event: StatChangedEvent):
    stat_changed_collection.insert_one(event.dict())
    return {"message": "OK"}


@app.post("/api/v1/event/grand-exchange-offer-changed")
async def grand_exchange_offer_change(event: GrandExchangeOfferChangedEvent):
    grand_exchange_offer_changed_collection.insert_one(event.dict())
    return {"message": "OK"}


@app.post("/api/v1/event/hitsplat-applied")
async def hitsplat_applied(event: HitsplatAppliedEvent):
    hitsplat_applied_collection.insert_one(event.dict())
    return {"message": "OK"}


@app.post("/api/v1/event/actor-death")
async def actor_death(event: ActorDeathEvent):
    actor_death_collection.insert_one(event.dict())
    return {"message": "OK"}


def main():
    from uvicorn import run
    run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
