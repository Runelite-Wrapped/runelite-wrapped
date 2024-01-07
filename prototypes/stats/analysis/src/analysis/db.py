import sqlite3
import json

_ENERGY_QUERY = """\
SELECT JSON_EXTRACT(JSON(data), '$.timestamp', '$.data.energy') FROM game_tick
"""
_TILE_QUERY = """\
SELECT JSON_EXTRACT(JSON(data), '$.timestamp', '$.data.location.x','$.data.location.y', '$.data.location.regionId') FROM game_tick
"""

class DbClient:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)

    def _execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [json.loads(x[0]) for x in cursor.fetchall()]

    def get_game_tick_data(self):
        result = self._execute_query(_ENERGY_QUERY)
        return {
            "timestamps": [int(x[0]) for x in result],
            "runEnergy": [int(x[1]) / 100 for x in result],
        }
    
    def get_tile_data(self):
        result = self._execute_query(_TILE_QUERY)
        return {
            "timestamps": [int(x[0]) for x in result],
            "xcoord": [int(x[1]) for x in result],
            "ycoord": [int(x[2]) for x in result],
            "regionId": [int(x[3]) for x in result],
        }
class AnalyticsClient:
    def __init__(self, db_file):
        self.db_client = DbClient(db_file)

    def get_combined_data(self):
        game_tick_data = self.db_client.get_game_tick_data()
        tile_data = self.db_client.get_tile_data()

        return {
            "gameTickData": game_tick_data,
            "tileData": tile_data
        }
    
    # todo    
    # def calculate_tile_count(
    #         username: str,
    #         db_client: DbClient
    #         ):
    #     game_tick_data = db_client.get_tile_data(username)

    #     tiles_moved = 0
    #     tile_counts = {}
    #     prev_x = prev_y = prev_region_id = None

    #     for tick in game_tick_data:
    #         _, _, _, x, y, region_id = tick
    #         tile = (x, y)

    #         tile_counts[tile] = tile_counts.get(tile, 0) + 1

    #         if prev_x is not None and prev_y is not None:
    #             dx = abs(x - prev_x)
    #             dy = abs(y - prev_y)
    #             dr = abs(region_id - prev_region_id) if prev_region_id is not None else 0

    #             if dx <= 2 and dy <= 2 or dr == 0:
    #                 tiles_moved += max(dx, dy)

    #         prev_x, prev_y, prev_region_id = x, y, region_id

    #     favourite_tile = max(tile_counts, key=tile_counts.get)

    #     return {
    #         "tilecount": tiles_moved,
    #         "username": username,
    #         "favourite_tile": favourite_tile,
    #     }


