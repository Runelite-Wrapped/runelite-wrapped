from typing import List, Optional
from pydantic import BaseModel


class LocationData(BaseModel):
    x: int
    y: int
    regionId: int


class ItemStackData(BaseModel):
    id: int
    quantity: int


class ActorData(BaseModel):
    combatLevel: int
    location: LocationData
    name: str
    type: int
    id: int


class GameTickData(BaseModel):
    energy: int
    health: int
    prayer: int
    sessionTickCount: int
    location: LocationData
    equipmentIds: Optional[List[int]] = None


class StatChangedData(BaseModel):
    boostedLevel: int
    level: int
    skill: str
    xp: int


class OfferData(BaseModel):
    itemId: int
    price: int
    quantitySold: int
    spent: int
    state: str
    totalQuantity: int


class GrandExchangeOfferData(BaseModel):
    offer: OfferData
    slot: int


class HitsplatData(BaseModel):
    amount: int
    disappearsOnGameCycle: int
    hitsplatType: int
    mine: bool
    others: bool


class HitsplatAppliedData(BaseModel):
    actor: ActorData
    hitsplat: HitsplatData


class ActorDeathData(BaseModel):
    combatLevel: int
    location: LocationData
    name: str


class LootReceivedData(BaseModel):
    actor: ActorData
    items: List[ItemStackData]


class GameEventBase(BaseModel):
    event: str
    timestamp: int
    username: str
    tickCount: int
    sessionId: str


class GameTickEvent(GameEventBase):
    data: GameTickData


class StatChangedEvent(GameEventBase):
    data: StatChangedData


class GrandExchangeOfferChangedEvent(GameEventBase):
    data: GrandExchangeOfferData


class HitsplatAppliedEvent(GameEventBase):
    data: HitsplatAppliedData


class ActorDeathEvent(GameEventBase):
    data: ActorDeathData


class LootReceivedEvent(GameEventBase):
    data: LootReceivedData
