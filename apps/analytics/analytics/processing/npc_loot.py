import time
from typing import Dict

import pandas as pd
from models.items import OsrsItemDb
from models.analytics import ItemLoot, NpcLoot, UserNpcLoot

from analytics.mongo import RawDbClient, AnalyticsDbClient


def calculate_npc_loot_for_user(
    username: str,
    osrs_item_db: OsrsItemDb,
    npc_id_name_map: Dict[int, str],
    raw_db_client: RawDbClient,
) -> None:
    gt_col = raw_db_client.get_loot_received_collection()

    # get all data.equipmentIds for this user, including duplicates
    username_npc_filter = {
        "username": username,
        "data.actor.type": 1,
    }

    # probably depending on mongo too much here
    npc_kill_counts = {
        npc["_id"]: npc["count"]
        for npc in gt_col.aggregate(
            [
                {"$match": username_npc_filter},
                {"$group": {"_id": "$data.actor.id", "count": {"$sum": 1}}},
            ]
        )
    }

    npc_loots = gt_col.find(
        username_npc_filter,
    )

    # convert to a pandas dataframe
    loot_df = pd.DataFrame(
        [
            {
                "npc_id": loot_received_data["data"]["actor"]["id"],
                "item_id": item["id"],
                "quantity": item["quantity"],
            }
            for loot_received_data in npc_loots
            for item in loot_received_data["data"]["items"]
        ]
    )

    if loot_df.empty:
        return UserNpcLoot(
            timestamp=time.time(),
            username=username,
            value=[],
        )

    loot_data = (
        loot_df.groupby(["npc_id", "item_id"])
        .sum()
        .reset_index()
        .groupby("npc_id")[["item_id", "quantity"]]
        .apply(lambda grp: dict(zip(grp["item_id"], grp["quantity"])))
        .to_dict()
    )

    # TODO(j.swannack): abstract getting the item from the item id and npc from the npc id
    return UserNpcLoot(
        timestamp=time.time(),
        username=username,
        value=[
            NpcLoot(
                id=npc_id,
                name=npc_id_name_map.get(npc_id, f"unknown-{npc_id}"),
                kill_count=npc_kill_counts.get(npc_id, 0),
                loot=[
                    ItemLoot(
                        # will raise error if item_id is not in osrs_item_db
                        # might happen if osrsbox db is out of date
                        item=osrs_item_db[item_id],
                        quantity=quantity,
                    )
                    for item_id, quantity in npc_loot.items()
                ],
            )
            for npc_id, npc_loot in loot_data.items()
        ],
    )


def load_npc_loot_for_user(
    user_npc_loot: UserNpcLoot,
    analytics_db_client: AnalyticsDbClient,
):
    analytics_db_client.get_npc_loot_collection().insert_one(user_npc_loot.dict())
