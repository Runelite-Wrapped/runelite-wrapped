from typing import Dict

import requests
from models.items import OsrsItemDb, parse_osrsbox_db

OSRSBOX_URL = "https://www.osrsbox.com/osrsbox-db/items-search.json"


def get_osrsbox_db() -> OsrsItemDb:
    response = requests.get(OSRSBOX_URL)
    response.raise_for_status()
    return parse_osrsbox_db(response.json())
