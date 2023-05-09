from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi import FastAPI
from dotenv import load_dotenv
import pymongo
import datetime
import pprint
import os

load_dotenv()

URI = os.environ["MONGO_URI"]

client = MongoClient(URI)
db = client.get_database("runelite-wrapped-raw")
game_tick_collection = db.get_collection("game_ticks")

app = FastAPI()


@app.post("/api/v1/event/game-tick/")
async def game_tick(event: dict):
    print(game_tick_collection.insert_one(event))
    return {"message": "OK"}
