from typing import Dict
from pydantic import parse_obj_as

import requests

RUNELOCUS_URL = "https://www.runelocus.com/addons/idlists/npcs-summary.json"


def get_npc_id_name_map() -> Dict[int, str]:
    response = requests.get(RUNELOCUS_URL)
    response.raise_for_status()

    return parse_obj_as(
        Dict[int, str], {k: v["name"] for k, v in response.json().items()}
    )
