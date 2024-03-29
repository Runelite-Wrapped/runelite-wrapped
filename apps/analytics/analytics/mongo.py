import os

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

_URI = os.environ["MONGO_URI"]

_RAW_DB_NAME = "runelite-wrapped-raw"
_ANALYTICS_DB_NAME = "runelite-wrapped-analytics"


_RAW_GAME_TICK_COLLECTION_NAME = "game_ticks"
_RAW_LOOT_RECEIVED_COLLECTION_NAME = "loot_received"
_RAW_HISCORES_COLLECTION_NAME = "hiscores"
_RAW_ACTOR_DEATH_COLLECTION_NAME = "actor_death"


_ANALYTICS_TOTAL_TICKS_COLLECTION_NAME = "total_ticks"
_ANALYTICS_USER_EQUIPMENT_COUNT_COLLECTION_NAME = "user_equipment_count"
_ANALYTICS_NPC_LOOT_COLLECTION_NAME = "npc_loot"
_ANALYTICS_USER_DEATH_COLLECTION_NAME = "user_death"
_ANALYTICS_TOTAL_TILES_COLLECTION_NAME = "total_tiles"
_ANALYTICS_HISCORES_GAINS_COLLECTION_NAME = "hiscores_gains"


class RawDbClient:
    def __init__(self, uri: str = None):
        self._uri = uri or _URI
        self.client = MongoClient(self._uri)

    def _get_raw_db(self) -> Database:
        return self.client.get_database(_RAW_DB_NAME)

    def get_game_tick_collection(self) -> Collection:
        return self._get_raw_db().get_collection(_RAW_GAME_TICK_COLLECTION_NAME)

    def get_loot_received_collection(self) -> Collection:
        return self._get_raw_db().get_collection(_RAW_LOOT_RECEIVED_COLLECTION_NAME)

    def get_hiscores_collection(self) -> Collection:
        return self._get_raw_db().get_collection(_RAW_HISCORES_COLLECTION_NAME)

    def get_actor_death_collection(self) -> Collection:
        return self._get_raw_db().get_collection(_RAW_ACTOR_DEATH_COLLECTION_NAME)


class AnalyticsDbClient:
    def __init__(self, uri: str = None):
        self._uri = uri or _URI
        self.client = MongoClient(self._uri)

    def _get_analytics_db(self) -> Database:
        return self.client.get_database(_ANALYTICS_DB_NAME)

    def get_total_tick_collection(self) -> Collection:
        return self._get_analytics_db().get_collection(
            _ANALYTICS_TOTAL_TICKS_COLLECTION_NAME
        )

    def get_user_equipment_count_collection(self) -> Collection:
        return self._get_analytics_db().get_collection(
            _ANALYTICS_USER_EQUIPMENT_COUNT_COLLECTION_NAME
        )

    def get_npc_loot_collection(self) -> Collection:
        return self._get_analytics_db().get_collection(
            _ANALYTICS_NPC_LOOT_COLLECTION_NAME
        )

    def get_user_death_collection(self) -> Collection:
        return self._get_analytics_db().get_collection(
            _ANALYTICS_USER_DEATH_COLLECTION_NAME
        )

    def get_total_tile_collection(self) -> Collection:
        return self._get_analytics_db().get_collection(
            _ANALYTICS_TOTAL_TILES_COLLECTION_NAME
        )

    def get_hiscores_gains_collection(self) -> Collection:
        return self._get_analytics_db().get_collection(
            _ANALYTICS_HISCORES_GAINS_COLLECTION_NAME
        )
