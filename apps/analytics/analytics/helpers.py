from typing import List
from analytics.mongo import RawDbClient


def get_all_usernames(raw_db_client: RawDbClient) -> List[str]:
    return raw_db_client.get_game_tick_collection().distinct("username")
