from typing import List, Optional
from analytics.mongo import RawDbClient

from common.models.items import OsrsItemDb, OsrsItem


def get_all_usernames(raw_db_client: RawDbClient) -> List[str]:
    return raw_db_client.get_game_tick_collection().distinct("username")


def get_item_from_equipment_id(
    equipment_id: int,
    osrs_item_db: OsrsItemDb,
) -> Optional[OsrsItem]:
    # Some weirdness with these IDs, see the comment below. (We don't care about the kit IDs, thats
    # like "LEGS", "TORSO", etc)
    # > If the ID for a specific slot is between 256 and 512, subtracting 256 will result in the
    #   kit ID. Values above 512 indicate an item and can be converted to the item ID by
    #   subtracting 512.
    # https://static.runelite.net/api/runelite-api/net/runelite/api/PlayerComposition.html
    if equipment_id <= 512:
        return None

    item_id = equipment_id - 512

    if item_id not in osrs_item_db:
        raise ValueError(f"Item ID {item_id} not found in OSRS item DB")

    return osrs_item_db.get(item_id)
