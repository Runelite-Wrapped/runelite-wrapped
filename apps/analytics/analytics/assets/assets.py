from typing import List, Dict
from dagster import asset, get_dagster_logger

from analytics.extract.items import get_osrsbox_db
from analytics.extract.bosses import get_boss_list
from analytics.extract.hiscores import get_user_hiscores_info, load_user_hiscores
from models.items import OsrsItemDb

from analytics.extract.items import get_osrsbox_db
from analytics.extract.npcs import get_npc_id_name_map

from analytics.processing.tick_count import (
    calculate_all_user_tick_counts,
    load_all_user_tick_counts,
)

from analytics.processing.equipment import (
    calculate_equipment_tick_counts_for_user,
    load_equipment_tick_counts_for_user,
)

from analytics.processing.npc_loot import (
    calculate_npc_loot_for_user,
    load_npc_loot_for_user,
)
from analytics.processing.usernames import get_all_usernames
from analytics.resources import MongoClient

_logger = get_dagster_logger(__name__)


@asset()
def boss_list() -> List[str]:
    return get_boss_list()


@asset()
def scrape_hiscores(
    usernames: List[str],
    boss_list: List[str],
    mongo_client: MongoClient,
):
    # TODO(j.swannack): consider using multiprocessing to speed this up
    for username in usernames:
        user_hiscores_info = get_user_hiscores_info(
            username=username, boss_list=boss_list
        )
        _logger.info(f"Got hiscores for {username}")
        load_user_hiscores(
            user_hiscores_info=user_hiscores_info,
            raw_db_client=mongo_client.get_raw_client(),
        )


@asset()
def usernames(mongo_client: MongoClient) -> list[str]:
    return get_all_usernames(mongo_client.get_raw_client())


@asset()
def osrs_item_db() -> OsrsItemDb:
    return get_osrsbox_db()


@asset()
def npc_id_name_map() -> Dict[int, str]:
    return get_npc_id_name_map()


@asset
def tick_count(
    usernames: List[str],
    mongo_client: MongoClient,
):
    tick_counts = calculate_all_user_tick_counts(
        usernames=usernames,
        raw_db_client=mongo_client.get_raw_client(),
    )
    _logger.info(f"Calculated tick counts for {len(tick_counts)} users")

    load_all_user_tick_counts(
        tick_counts,
        analytics_db_client=mongo_client.get_analytics_client(),
    )
    _logger.info(f"Loaded tick counts for {len(tick_counts)} users")


@asset()
def equipment_analysis(
    osrs_item_db: OsrsItemDb,
    usernames: List[str],
    mongo_client: MongoClient,
):
    """
    Counts the number of game ticks a player has spent wearing each piece of equipment.
    """

    raw_db_client = mongo_client.get_raw_client()
    analytics_db_client = mongo_client.get_analytics_client()

    for username in usernames:
        user_equipment_count = calculate_equipment_tick_counts_for_user(
            username=username,
            raw_db_client=raw_db_client,
            osrs_item_db=osrs_item_db,
        )
        load_equipment_tick_counts_for_user(
            user_equipment_count=user_equipment_count,
            analytics_db_client=analytics_db_client,
        )


@asset()
def npc_loot(
    usernames: List[str],
    osrs_item_db: OsrsItemDb,
    npc_id_name_map: Dict[int, str],
    mongo_client: MongoClient,
):
    for username in usernames:
        user_npc_loot = calculate_npc_loot_for_user(
            username=username,
            osrs_item_db=osrs_item_db,
            npc_id_name_map=npc_id_name_map,
            raw_db_client=mongo_client.get_raw_client(),
        )
        load_npc_loot_for_user(
            user_npc_loot=user_npc_loot,
            analytics_db_client=mongo_client.get_analytics_client(),
        )
