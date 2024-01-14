import pandas as pd

def calculate_tile_count(username: str, tile_data) -> dict:
    game_tick_data = tile_data
    gtdf = pd.DataFrame(game_tick_data, columns=['regionId','timestamp', 'xcoord', 'ycoord'])
    gtdf.rename(columns={'xcoord': 'x', 'ycoord': 'y'}, inplace=True)

    # Extract 'tile' as a tuple of x and y coordinates
    gtdf['tile'] = list(zip(gtdf['x'], gtdf['y']))

    # Calculate changes (deltas) in x, y, and regionId
    gtdf['dx'] = gtdf['x'].diff().abs().fillna(0)
    gtdf['dy'] = gtdf['y'].diff().abs().fillna(0)
    gtdf['dr'] = gtdf['regionId'].diff().abs().fillna(0)

    # Calculate tiles moved
    gtdf['tiles_moved'] = gtdf[['dx', 'dy']].max(axis=1)
    # Adjust tiles_moved for large changes (non-walking movement)
    gtdf.loc[((gtdf['dx'] > 2) | (gtdf['dy'] > 2)) & (gtdf['dr'] != 0), 'tiles_moved'] = 0

    # Calculate the favourite tile and total tiles moved
    favourite_tile = gtdf['tile'].value_counts().idxmax()
    tiles_moved = gtdf['tiles_moved'].sum()


    # convert to native Python types for JSON seriallisation
    tiles_moved = int(tiles_moved)

    if isinstance(favourite_tile, tuple):
            # Convert elements to int, handling NaN values
            favourite_tile = tuple(int(x) if x == x else None for x in favourite_tile)
            # x == x will be False if x is NaN

    return {
        "tilecount": tiles_moved,
        "username": username,
        "favourite_tile": favourite_tile,
    }

def calculate_all_user_tiles_moved(usernames, db_client):
    return {
        username: calculate_tile_count(username, db_client)
        for username in usernames
    }
