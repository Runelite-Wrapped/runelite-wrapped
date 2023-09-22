from typing import Dict
from pydantic import BaseModel, parse_obj_as


class OsrsItem(BaseModel):
    id: int
    name: str
    type: str
    duplicate: bool


def parse_osrsbox_db(data: dict) -> Dict[int, OsrsItem]:
    return parse_obj_as(Dict[int, OsrsItem], data)
