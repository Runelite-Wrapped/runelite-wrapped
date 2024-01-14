# loads in sqlite db and lists the tables

import json
from analysis.constants import DB_FILE
from analysis.db import DbClient
from analysis.db import AnalyticsClient

def get_tile_data(username):
    analytics_client = AnalyticsClient(DB_FILE)
    tile_data = analytics_client.db_client.get_tile_data()
    return json.dumps(tile_data)

def get_energy_data(username):
    analytics_client = AnalyticsClient(DB_FILE)
    energy_data = analytics_client.db_client.get_energy_data()
    return json.dumps(energy_data)

def calculate_tile_count(username):
    analytics_client = AnalyticsClient(DB_FILE)
    tile_count_data = analytics_client.calculate_tile_count_for_user(username)
    return json.dumps(tile_count_data)

def main():
    db_client = DbClient(DB_FILE)
    energy_data = db_client.get_energy_data()
    tile_data = db_client.get_tile_data()
    tile_count = db_client.calculate_tile_count()

    combined_data = {
        "energyData": energy_data,
        "tileData": tile_data
    }
    return json.dumps(combined_data)
