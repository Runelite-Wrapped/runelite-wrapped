from typing import List
from pathlib import Path
from pymongo import MongoClient
from bson.objectid import ObjectId
from requests import post
from pprint import pprint
import pymongo
import datetime
import os
import json


_script_dir = Path(__file__).parent.absolute()
_data_dir = _script_dir.parent / "data"

URI = os.environ["MONGO_URI"]


def _load_data(filename) -> List[dict]:
    """Load file using json"""
    with open(filename) as f:
        return json.load(f)


def _get_inputs_collection():
    client = MongoClient(URI)
    db = client.get_database("runelite-wrapped-testing")
    inputs = db.get_collection("inputs")
    return inputs


def main():
    data = _load_data(_data_dir / "test_game_ticks.json")
    inputs = _get_inputs_collection()
    return inputs.insert_many(data)

    # for game_tick in data:
    #    pprint(inputs.insert_one(game_tick))


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
