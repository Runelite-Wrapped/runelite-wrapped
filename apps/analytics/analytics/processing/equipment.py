import pandas as pd
import time

from models.items import OsrsItemDb
from models.analytics import EquipmentCount, SlotEquipmentCount, UserEquipmentCount

from analytics.helpers import get_item_from_equipment_id
from analytics.mongo import RawDbClient


def calculate_equipment_tick_counts_for_user(
    username: str,
    raw_db_client: RawDbClient,
    osrs_item_db: OsrsItemDb,
) -> UserEquipmentCount:
    gt_col = raw_db_client.get_game_tick_collection()

    # get all data.equipmentIds for this user, including duplicates
    equipment_ids = gt_col.find(
        {"username": username},
        {"data.equipmentIds": 1},
    )

    # convert to a pandas dataframe
    equipment_ids_df = pd.DataFrame(
        map(lambda x: x["data"]["equipmentIds"], equipment_ids)
    )

    # for each column get the count of each unique value
    equipment_ids_counts = [
        equipment_ids_df[col].value_counts().to_dict() for col in equipment_ids_df
    ]

    # for each column, convert the equipment id to the item name
    return UserEquipmentCount(
        value=[
            SlotEquipmentCount(
                counts=sorted(
                    [
                        EquipmentCount(
                            **{
                                "item": get_item_from_equipment_id(
                                    equipment_id, osrs_item_db
                                ),
                                "count": count,
                            }
                        )
                        for equipment_id, count in count_list.items()
                    ],
                    key=lambda v: v.count,
                )
            )
            for count_list in equipment_ids_counts
        ],
        timestamp=time.now(),
        username=username,
    )
