from typing import Dict, List

from pydantic import BaseModel

from models.items import OsrsItem


class AnalyticsLocationData(BaseModel):
    x: int
    y: int
    regionId: int
    name: str


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


class UserDeath(BaseModel):
    timestamp: float
    location_data: AnalyticsLocationData


class UserDeathStats(BaseModel):
    timestamp: float
    username: str
    value: List[UserDeath]


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


class UserDeath(BaseModel):
    timestamp: float
    location_data: AnalyticsLocationData


class UserDeathStats(BaseModel):
    timestamp: float
    username: str
    value: List[UserDeath]


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


class UserDeath(BaseModel):
    timestamp: float
    location_data: AnalyticsLocationData


class UserDeathStats(BaseModel):
    timestamp: float
    username: str
    value: List[UserDeath]

class LocationData(BaseModel):
    x: int
    y: int
    regionId: int
class TileCount(BaseModel):
    timestamp: float
    tilecount: int
    username: str
    favourite_tile: object