import time
import pandas as pd

from typing import Dict, List
from collections import Counter

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

    ########### build initial DF
    gtdf = pd.DataFrame(game_tick_data)

    gtdf['energy'] = gtdf['data'].apply(lambda row: row['energy'])
    gtdf['sessionTickCount'] = gtdf['data'].apply(lambda row: row['sessionTickCount'])
    gtdf['x'] = gtdf['data'].apply(lambda row: row['location']['x'] if 'location' in row and 'x' in row['location'] else None)
    gtdf['y'] = gtdf['data'].apply(lambda row: row['location']['y'] if 'location' in row and 'y' in row['location'] else None)
    gtdf['regionId'] = gtdf['data'].apply(lambda row: row['location']['regionId'] if 'location' in row and 'regionId' in row['location'] else None)
    gtdf['tile'] = list(zip(gtdf['x'], gtdf['y']))


    gtdf.dropna(subset=['regionId'], inplace=True)
    gtdf = gtdf.drop(columns=['data'])

    ### change in x coord
    gtdf['dx'] = (gtdf['x'].abs() - gtdf['x'].shift(1).abs()).abs().fillna(0)
    ### change in y coord
    gtdf['dy'] = (gtdf['y'].abs() - gtdf['y'].shift(1).abs()).abs().fillna(0)
    ### change in timestamp - should roughly reflect tick length
    gtdf['dt'] = (gtdf['timestamp'] - gtdf['timestamp'].shift(1)).abs().fillna(0)
    ### change in regionId - large changes indicate non-walking movement i.e new area door, or teleportation 
    gtdf['dr'] = (gtdf['regionId'] - gtdf['regionId'].shift(1)).abs().fillna(0)

    ########### calculate tiles moved
    def calc_tiles_moved(row):
        if row['dx'] == 0 and row['dy'] == 0:
            return 0
        elif (((row['dx'] > 2) or (row['dy'] > 2)) and row['dr'] > 0):
            return 0
        # elif (((row['dx'] > 2) or (row['dy'] > 2)) and row['dr'] == 0):
        #     return abs(row['dx']) + abs(row['dy'])
        elif (row['dx'] != 0) or (row['dy'] != 0):
            return max(abs(row['dx']), abs(row['dy']))
        else:
            return "Error"
        
    gtdf['tiles_moved'] = gtdf.apply(calc_tiles_moved, axis=1)

    ### TODO type favourite_tile as AnalyticsLocationData
    favourite_tile = gtdf['tile'].value_counts().idxmax()
    tiles_moved = gtdf['tiles_moved'].sum()

    #########################################################################################################
    #################### some debugging:

    ####################
    tdf = gtdf.copy()

    tiles_moved_mask = tdf['tiles_moved'] > 4

    previous_row = tiles_moved_mask.shift(-1, fill_value=False)
    next_row = tiles_moved_mask.shift(1, fill_value=False)
    second_next_row = tiles_moved_mask.shift(2, fill_value=False)

    tm_combined_condition = (
        tiles_moved_mask | previous_row | next_row | second_next_row
    )

    tdf = tdf[tiles_moved_mask]

    print('tiles moved debug')
    print(tdf)

    #########################################################################################################

    # Filter rows based on the combined condition for gtdf

    print("full df is: ")
    print(gtdf)

    #########################################################################################################
    #########################################################################################################

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
    print(outputs)
    return outputs


def load_all_user_tile_counts(
    tiles_moved_per_account: Dict[str, TileCount],
    analytics_db_client: AnalyticsDbClient,
) -> dict:
    return analytics_db_client.get_total_tick_collection().insert_many(
        [tick_count.dict() for tick_count in tiles_moved_per_account.values()]
    )


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    calculate_all_user_tiles_moved()