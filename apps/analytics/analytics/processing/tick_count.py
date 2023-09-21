import time
from typing import Dict

from analytics.helpers import get_all_usernames
from analytics.mongo import RawDbClient, AnalyticsDbClient

from models.analytics import TickCount


def calculate_tick_count(
    username: str,
    raw_db_client: RawDbClient,
) -> TickCount:
    game_tick_count = raw_db_client.get_game_tick_collection().count_documents(
        {
            "username": username,
        }
    )

    return TickCount(
        **{
            "timestamp": time.time(),
            "value": game_tick_count,
            "username": username,
        }
    )


def calculate_all_user_tick_counts(
    raw_db_client: RawDbClient = None,
) -> Dict[str, TickCount]:
    usernames = get_all_usernames(raw_db_client)
    outputs = {
        username: calculate_tick_count(
            username,
            raw_db_client,
        )
        for username in usernames
    }

    return outputs


def load_all_user_tick_counts(
    tick_counts_per_account: Dict[str, TickCount],
    analytics_db_client: AnalyticsDbClient,
) -> dict:
    return analytics_db_client.get_total_tick_collection().insert_many(
        [tick_count.dict() for tick_count in tick_counts_per_account.values()]
    )


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    calculate_all_user_tick_counts()
