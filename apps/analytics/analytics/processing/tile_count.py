import time
import pandas as pd
from typing import Dict, List

from analytics.mongo import RawDbClient, AnalyticsDbClient
from models.analytics import TileCount

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 800) 
pd.set_option('display.max_rows', 150)  # display up to 200 rows

def calculate_tile_count(
    username: str,
    raw_db_client: RawDbClient,
) -> TileCount:
    game_tick_data = raw_db_client.get_game_tick_collection().find(
        {
            "username": username,
        }
    )

    ### build initial DF
    gtdf = pd.DataFrame(game_tick_data)

    gtdf['energy'] = gtdf['data'].apply(lambda row: row['energy'])
    gtdf['sessionTickCount'] = gtdf['data'].apply(lambda row: row['sessionTickCount'])
    gtdf['x'] = gtdf['data'].apply(lambda row: row['location']['x'])
    gtdf['y'] = gtdf['data'].apply(lambda row: row['location']['y'])
    gtdf['regionId'] = gtdf['data'].apply(lambda row: row['location']['regionId'])
    gtdf['tile'] = list(zip(gtdf['x'], gtdf['y']))

    gtdf = gtdf.drop(columns=['data'])

    ### change in x coord
    gtdf['dx'] = gtdf["x"].abs().diff().abs().fillna(0)
    ### change in y coord
    gtdf['dy'] = gtdf["y"].abs().diff().abs().fillna(0)
    ### change in timestamp - should roughly reflect tick length
    gtdf['dt'] = gtdf["regionId"].diff().abs().fillna(0)
    ### change in regionId - large changes indicate non-walking movement i.e new area door, or teleportation 
    gtdf['dr'] = gtdf["regionId"].diff().abs().fillna(0)

    ### updated tiles moved
    gtdf['tiles_moved'] = gtdf[['dx', 'dy']].max(axis=1)
    gtdf.loc[((gtdf['dx'] > 2) | (gtdf['dy'] > 2)) & (gtdf['dr'] != 0), 'tiles_moved'] = 0

    ### TODO type favourite_tile as AnalyticsLocationData
    favourite_tile = gtdf['tile'].value_counts().idxmax()
    tiles_moved = gtdf['tiles_moved'].sum()

    return TileCount(
        **{
            "timestamp": time.time(),
            "tilecount": tiles_moved,
            "username": username,
            "favourite_tile": favourite_tile,
        }
    )

def calculate_all_user_tiles_moved(
    usernames: List[str],
    raw_db_client: RawDbClient = None,
) -> Dict[str, TileCount]:
    outputs = {
        username: calculate_tile_count(
            username=username,
            raw_db_client=raw_db_client,
        )
        for username in usernames
    }
    return outputs

def load_all_user_tile_counts(
    tiles_moved_per_account: Dict[str, TileCount],
    analytics_db_client: AnalyticsDbClient,
) -> dict:
    return analytics_db_client.get_total_tile_collection().insert_many(
        [tick_count.dict() for tick_count in tiles_moved_per_account.values()]
    )

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    calculate_all_user_tiles_moved()