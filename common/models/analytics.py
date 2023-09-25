from typing import Dict, List

from pydantic import BaseModel

from models.items import OsrsItem


class TickCount(BaseModel):
    timestamp: float
    value: int
    username: str


class EquipmentCount(BaseModel):
    item: OsrsItem
    count: int


class SlotEquipmentCount(BaseModel):
    counts: List[EquipmentCount]


class UserEquipmentCount(BaseModel):
    timestamp: float
    value: List[SlotEquipmentCount]
    username: str
