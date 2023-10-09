from typing import Dict
from pydantic import parse_obj_as

import requests

RUNELOCUS_URL = "https://www.runelocus.com/addons/idlists/npcs-summary.json"
WIKI_URL_BASE = "https://oldschool.runescape.wiki/"


# TODO(jerome3o): would be good to also get combat level (to make image collection easier)
def get_npc_id_name_map() -> Dict[int, str]:
    response = requests.get(RUNELOCUS_URL)
    response.raise_for_status()

    return parse_obj_as(
        Dict[int, str], {k: v["name"] for k, v in response.json().items()}
    )


def guess_npc_wiki_url(
    npc_name: str,
    combat_level: int = None,
):
    url = f"{WIKI_URL_BASE}w/{npc_name.replace(' ', '_')}"

    if combat_level is not None:
        url += f"#Level_{combat_level}"

    return url


def guess_npc_wiki_image(
    npc_name: str,
    combat_level: int = None,
):
    # https://oldschool.runescape.wiki/images/Zombie_(Level_76).png
    url = f"{WIKI_URL_BASE}images/{npc_name.replace(' ', '_')}"

    if combat_level is not None:
        url += f"_(Level_{combat_level})"

    url += ".png"

    return url


def scrape_npc_wiki_for_image(npc_name: str):
    # TODO(jerome3o): implement
    pass
