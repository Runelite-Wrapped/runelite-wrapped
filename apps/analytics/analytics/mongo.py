import os

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

_URI = os.environ["MONGO_URI"]

_RAW_DB_NAME = "runelite-wrapped-raw"
_ANALYTICS_DB_NAME = "runelite-wrapped-analytics"

_GAME_TICK_COLLECTION_NAME = "game_ticks"


class RawDbClient:
    def __init__(self, uri: str = None):
        self._uri = uri or _URI
        self.client = MongoClient(self._uri)

    def _get_raw_db(self) -> Database:
        return self.client.get_database(_RAW_DB_NAME)

    def get_game_tick_collection(self) -> Collection:
        return self._get_raw_db().get_collection(_GAME_TICK_COLLECTION_NAME)


class AnalyticsDbClient:
    def __init__(self, uri: str = None):
        self._uri = uri or _URI
        self.client = MongoClient(self._uri)

    def _get_analytics_db(self) -> Database:
        return self.client.get_database(_ANALYTICS_DB_NAME)

    def get_total_tick_collection(self) -> Collection:
        return self._get_analytics_db().get_collection("total_ticks")
