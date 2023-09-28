from typing import Optional
from pydantic import BaseModel


class StatInfo(BaseModel):
    rank: int
    level: int
    experience: int
    next_level_exp: Optional[int]
    exp_to_next_level: Optional[int]


class BossInfo(BaseModel):
    rank: int
    kills: int


class UserHiscoresInfo(BaseModel):
    username: str
    timestamp: float
    skills: dict[str, StatInfo]
    bosses: dict[str, BossInfo]


class OsrsScrape(BaseModel):
    timestamp: float
    users: list[UserHiscoresInfo]
