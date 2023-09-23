import pandas as pd

from analytics.mongo import RawDbClient


def calculate_equipment_tick_counts_for_user(
    username: str,
    raw_db_client: RawDbClient,
):
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

    return equipment_ids_counts
