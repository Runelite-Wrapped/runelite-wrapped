import os

import time
import requests
from dotenv import load_dotenv

load_dotenv()
SERVER_IP = os.environ["SERVER_IP"]

_URL = f"http://{SERVER_IP}:8000/api/v1/event/game-tick/"

# Example tick data:
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

# Example stat-changed data:
#   {
#     "data": {
#       "boostedLevel": 99,
#       "level": 99,
#       "skill": "ATTACK",
#       "xp": 21245442
#     },
#     "event": "stat-changed",
#     "timestamp": 1683933323624,
#     "username": "jerome-o"
#   }

# Example grand-exchange-offer-changed
#   {
#     "data": {
#       "offer": {
#         "ab": 0,
#         "ac": 0,
#         "an": 0,
#         "au": 0,
#         "aw": 0,
#         "itemId": 0,
#         "price": 0,
#         "quantitySold": 0,
#         "spent": 0,
#         "state": "EMPTY",
#         "totalQuantity": 0
#       },
#       "slot": 0
#     },
#     "event": "grand-exchange-offer-changed",
#     "timestamp": 1683933323845,
#     "username": "jerome-o"
#   }


# Example hitsplat-applied data:
#   {
#     "data": {
#       "actor": {
#         "combatLevel": 124,
#         "location": {
#           "x": 6464,
#           "y": 6848
#         },
#         "name": "jerome-o"
#       },
#       "hitsplat": {
#         "amount": 10,
#         "disappearsOnGameCycle": 4666,
#         "hitsplatType": 16,
#         "mine": true,
#         "others": false
#       }
#     },
#     "event": "hitsplat-applied",
#     "timestamp": 1683933378913,
#     "username": "jerome-o"
#   }

# Example actor-death data:
#   {
#     "data": {
#       "combatLevel": 124,
#       "location": {
#         "x": 6464,
#         "y": 6720
#       },
#       "name": "jerome-o"
#     },
#     "event": "actor-death",
#     "timestamp": 1683933389115,
#     "username": "jerome-o"
#   }


def _make_sample_data(index: int) -> dict:
    # use the index to make a unique sample
    return {
        "data": {
            "energy": 10000 + index,
            "health": (50 + index) % 99,
            "prayer": (50 + index) % 85,
            "sessionTickCount": index,
            "x": 0 + index * 10,
            "y": 0 + index * 10,
        },
        "event": "game-tick",
        "timestamp": 1683158133517 + index * 600,
        "username": "jerome-o",
    }


def seed_forever():
    i = 0
    while True:
        try:
            sample = _make_sample_data(i)
            response = requests.post(_URL, json=sample)
            print(response.status_code)
            print(response.text)
            i += 1
            time.sleep(0.6)

        except Exception as e:
            print(f"Exception encountered {e}")
            time.sleep(0.6)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    seed_forever()
