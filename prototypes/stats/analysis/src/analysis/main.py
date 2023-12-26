# loads in sqlite db and lists the tables

import json
from analysis.constants import DB_FILE
from analysis.db import DbClient


def main():
    db_client = DbClient(DB_FILE)
    return json.dumps(db_client.get_game_tick_data())
