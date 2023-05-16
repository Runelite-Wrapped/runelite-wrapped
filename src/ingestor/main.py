import os

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


class GameEvent(BaseModel):
    data: BaseModel
    event: str
    timestamp: int
    username: str


class GameTickData(BaseModel):
    energy: int
    health: int
    prayer: int
    sessionTickCount: int
    x: int
    y: int


class GameEventData(BaseModel):
    data: GameTickData
    event: str
    timestamp: int
    username: str


class StatChangedData(BaseModel):
    boostedLevel: int
    level: int
    skill: str
    xp: int


class StatChangedEvent(BaseModel):
    data: StatChangedData
    event: str
    timestamp: int
    username: str


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


class GrandExchangeOfferChangedEvent(BaseModel):
    data: GrandExchangeOfferData
    event: str
    timestamp: int
    username: str


class LocationData(BaseModel):
    x: int
    y: int


class ActorData(BaseModel):
    combatLevel: int
    location: LocationData
    name: str


class HitsplatData(BaseModel):
    amount: int
    disappearsOnGameCycle: int
    hitsplatType: int
    mine: bool
    others: bool


class HitsplatAppliedData(BaseModel):
    actor: ActorData
    hitsplat: HitsplatData


class HitsplatAppliedEvent(BaseModel):
    data: HitsplatAppliedData
    event: str
    timestamp: int
    username: str


class ActorDeathData(BaseModel):
    combatLevel: int
    location: LocationData
    name: str


class ActorDeathEvent(BaseModel):
    data: ActorDeathData
    event: str
    timestamp: int
    username: str


@app.post("/api/v1/event/game-tick/")
async def game_tick(event: GameEventData):
    print(game_tick_collection.insert_one(event.dict()))
    return {"message": "OK"}


@app.post("/api/v1/event/stat-changed")
async def game_tick(event: StatChangedEvent):
    print(stat_changed_collection.insert_one(event.dict()))
    return {"message": "OK"}


@app.post("/api/v1/event/grand-exchange-offer-changed")
async def game_tick(event: GrandExchangeOfferChangedEvent):
    print(grand_exchange_offer_changed_collection.insert_one(event.dict()))
    return {"message": "OK"}


@app.post("/api/v1/event/hitsplat-applied")
async def game_tick(event: HitsplatAppliedEvent):
    print(hitsplat_applied_collection.insert_one(event.dict()))
    return {"message": "OK"}


@app.post("/api/v1/event/actor-death")
async def game_tick(event: ActorDeathEvent):
    print(actor_death_collection.insert_one(event.dict()))
    return {"message": "OK"}
