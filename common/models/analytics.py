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


class ItemLoot(BaseModel):
    item: OsrsItem
    quantity: int


class NpcLoot(BaseModel):
    name: str
    id: int
    kill_count: int
    loot: List[ItemLoot]


class UserNpcLoot(BaseModel):
    timestamp: float
    username: str
    value: List[NpcLoot]
