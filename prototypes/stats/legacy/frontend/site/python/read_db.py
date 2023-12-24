# loads in sqlite db and lists the tables

import json
import sqlite3

conn = sqlite3.connect("/stat.db")

c = conn.cursor()

c.execute("SELECT JSON(data) -> '$.timestamp' FROM game_tick")
print("hello")
result = c.fetchall()

timestamps = [int(x[0]) for x in result]
print(timestamps)


# TODO: find a way to pass data between without having
#   to (de)serialize
json.dumps(
    {
        "timestamps": timestamps,
    }
)
