# loads in sqlite db and lists the tables

import json
from analysis.constants import DB_FILE
from analysis.db import DbClient


def main():
    db_client = DbClient(DB_FILE)
    game_tick_data = db_client.get_game_tick_data()
    tile_data = db_client.get_tile_data()

    combined_data = {
        "gameTickData": game_tick_data,
        "tileData": tile_data
    }
    return json.dumps(combined_data)
