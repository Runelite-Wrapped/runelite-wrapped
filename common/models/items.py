from typing import Dict
from pydantic import BaseModel, parse_obj_as


class OsrsItem(BaseModel):
    id: int
    name: str
    type: str
    duplicate: bool


OsrsItemDb = Dict[int, OsrsItem]


def get_unknown_item(id: int) -> OsrsItem:
    return OsrsItem(
        id=id,
        name=f"Unknown Item {id}",
        type="Unknown",
        duplicate=False,
    )


def parse_osrsbox_db(data: dict) -> OsrsItemDb:
    return parse_obj_as(OsrsItemDb, data)
