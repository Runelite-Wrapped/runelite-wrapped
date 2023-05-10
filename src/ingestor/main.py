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

app = FastAPI()


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


@app.post("/api/v1/event/game-tick/")
async def game_tick(event: GameEventData):
    print(game_tick_collection.insert_one(event.dict()))
    return {"message": "OK"}
