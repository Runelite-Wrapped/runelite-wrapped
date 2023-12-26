import sqlite3
import json

_ENERGY_QUERY = """\
SELECT JSON_EXTRACT(JSON(data), '$.timestamp', '$.data.energy') FROM game_tick
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
