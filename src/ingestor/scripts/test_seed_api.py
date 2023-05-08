from typing import List
from pathlib import Path
import time
import json
import requests

_URL = "http://localhost:8000/api/v1/event/game-tick/"

# Example data:
# {
#     "data": {
#         "energy": 10000,
#         "health": 99,
#         "prayer": 85,
#         "sessionTickCount": 380,
#         "x": 8128,
#         "y": 3008
#     },
#     "event": "game-tick",
#     "timestamp": 1683158133517,
#     "username": "jerome-o"
# }


def _make_sample_data(index: int) -> dict:
    # use the index to make a unique sample
    return {
        "data": {
            "energy": 10000 + index,
            "health": (50 + index) % 99,
            "prayer": (50 + index) % 85,
            "sessionTickCount": index,
            "x": 0 + index*10,
            "y": 0 + index*10,
        },
        "event": "game-tick",
        "timestamp": 1683158133517 + index*600,
        "username": "jerome-o"
    }




_script_dir = Path(__file__).parent.absolute()
_data_dir = _script_dir.parent / 'data'


def _load_data(filename) -> List[dict]:
    """Load file using json"""
    with open(filename) as f:
        return json.load(f)


def main():
    data = _load_data(_data_dir / "test_game_ticks.json")

    for tick_data in data:
        response = requests.post(_URL, json=tick_data)
        print(response.status_code)
        print(response.text)


def seed_forever():

    i = 0
    while True:
        sample = _make_sample_data(i)
        response = requests.post(_URL, json=sample)
        print(response.status_code)
        print(response.text)
        i += 1
        time.sleep(0.6)



if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    seed_forever()
