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
total_tick_collection = db.get_collection("analytics.total_ticks")


def pull_game_tick_data(username: str):
    # Pull all game tick data for a certain player (username)
    # Calculate / count the number of gameticks
    # Push that to the analytics collection (total_tick_collection)

    # {
    # "stat": "total_ticks",
    # "timestamp": "{time stamp of calculation} i.e. use `import time; time.time()`",
    # "value": 23423,
    # }

    pass
