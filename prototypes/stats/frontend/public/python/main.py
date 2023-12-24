# loads in sqlite db and lists the tables

import json
import sqlite3

conn = sqlite3.connect("/stats.db")

c = conn.cursor()

c.execute("SELECT JSON_EXTRACT(JSON(data), '$.timestamp') FROM game_tick")
result = c.fetchall()

timestamps = [int(x[0]) for x in result]


# TODO: find a way to pass data between without having
#   to (de)serialize
json.dumps(
    {
        "timestamps": [1, 2, 3],
        "runEnergy": [1, 2, 3],
    }
)
