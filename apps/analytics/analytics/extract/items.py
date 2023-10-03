from bs4 import BeautifulSoup

import requests
from models.items import OsrsItemDb, parse_osrsbox_db

OSRSBOX_URL = "https://www.osrsbox.com/osrsbox-db/items-search.json"
RUNELITE_ITEM_DOCS_URL = (
    "https://static.runelite.net/api/runelite-api/constant-values.html"
)


def get_osrsbox_db() -> OsrsItemDb:
    response = requests.get(OSRSBOX_URL)
    response.raise_for_status()
    return parse_osrsbox_db(response.json())


def get_runelite_item_db() -> OsrsItemDb:
    html = requests.get(RUNELITE_ITEM_DOCS_URL).text
    soup = BeautifulSoup(html, "html.parser")
    return _parse_runelite_docs(soup)


def _parse_runelite_docs(soup: BeautifulSoup) -> OsrsItemDb:
    item_table: BeautifulSoup = None

    for li in soup.find_all("li", class_="blockList"):
        # Try to find the `a` element with innerHTML 'ItemID' within the current 'li' element
        item_id = li.select_one("table caption span a")

        # Check if the 'a' element exists and its text is 'ItemID'
        if item_id and item_id.text == "ItemID":
            # print the 'li' if found

            # break out of all loops
            item_table = li.select_one("table")
            break

    tbody = item_table.select_one("tbody")
    all_outputs = []
    trs = tbody.select("tr")
    for tr in trs:
        output = []
        output.append(
            tr.select_one("th.colSecond").select_one("code").select_one("a").text
        )
        output.append(tr.select_one("td.colLast").select_one("code").text)
        all_outputs.append(output)

    return parse_osrsbox_db(
        {
            int(id_str): {
                "id": int(id_str),
                "name": _java_to_human_item_name(name),
                "type": "Unknown",
                "duplicate": False,
            }
            for name, id_str in all_outputs
        }
    )


def _java_to_human_item_name(name: str) -> str:
    return name.replace("_", " ").strip().title()
