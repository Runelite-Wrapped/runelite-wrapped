from pydantic import BaseModel


class TickCount(BaseModel):
    timestamp: float
    value: int
    username: str
