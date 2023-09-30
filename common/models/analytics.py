from pydantic import BaseModel


class TickCount(BaseModel):
    timestamp: float
    value: int
    username: str

class LocationData(BaseModel):
    x: int
    y: int
    regionId: int
class TileCount(BaseModel):
    timestamp: float
    tilecount: int
    username: str
    favourite_tile: object