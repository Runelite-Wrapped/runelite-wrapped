from typing import List
from pymongo import MongoClient


def get_all_usernames(client: MongoClient) -> List[str]:
    db_raw = client.get_database("runelite-wrapped-raw")
    game_tick_collection = db_raw.get_collection("game_ticks")
    unique_usernames = game_tick_collection.distinct("username")

    return unique_usernames
