# loads in sqlite db and lists the tables

import json
from analysis.constants import DB_FILE
from analysis.db import DbClient
from analysis.db import AnalyticsClient


def get_tile_data():
    analytics_client = AnalyticsClient(DB_FILE)
    tile_data = analytics_client.db_client.get_tile_data()
    return json.dumps(tile_data)

def get_game_tick_data():
    analytics_client = AnalyticsClient(DB_FILE)
    game_tick_data = analytics_client.db_client.get_game_tick_data()
    return json.dumps(game_tick_data)

# todo
# def calculate_tile_count_for_user(username):
#     analytics_client = AnalyticsClient(DB_FILE)
#     tile_count_data = analytics_client.calculate_tile_count(username, analytics_client.db_client)
#     return json.dumps(tile_count_data)


def main():
    db_client = DbClient(DB_FILE)
    game_tick_data = db_client.get_game_tick_data()
    tile_data = db_client.get_tile_data()

    combined_data = {
        "gameTickData": game_tick_data,
        "tileData": tile_data
    }
    return json.dumps(combined_data)
