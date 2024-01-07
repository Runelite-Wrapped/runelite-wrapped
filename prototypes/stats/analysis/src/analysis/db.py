import sqlite3
import json

_ENERGY_QUERY = """\
SELECT JSON_EXTRACT(JSON(data), '$.timestamp', '$.data.energy') FROM game_tick
"""
_TILE_QUERY = """\
SELECT JSON_EXTRACT(JSON(data), '$.timestamp', '$.data.location.x','$.data.location.y', '$.data.location.regionId') from game_tick
"""


class DbClient:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)

    def get_game_tick_data(self):
        c = self.conn.cursor()
        c.execute(_ENERGY_QUERY)
        result = [json.loads(x[0]) for x in c.fetchall()]

        return {
            "timestamps": [int(x[0]) for x in result],
            "runEnergy": [int(x[1]) / 100 for x in result],
        }
    
    def get_tile_data(self):
        c = self.conn.cursor()
        c.execute(_TILE_QUERY)
        result = [json.loads(x[0]) for x in c.fetchall()]

        return {
            "timestamps": [int(x[0]) for x in result],
            "xcoord": [int(x[1]) for x in result],
            "ycoord": [int(x[2]) for x in result],
            "regionId": [int(x[3]) for x in result],
        }

class AnalyticsClient:
    def __init__(self, d_file)
