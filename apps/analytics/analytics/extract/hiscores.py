import time
from typing import List
from urllib.parse import quote

from OSRS_Hiscores import Hiscores
from models.hiscores import BossInfo, StatInfo, UserHiscoresInfo

from analytics.mongo import RawDbClient


def get_user_hiscores_info(username: str, boss_list: List[str]) -> UserHiscoresInfo:
    # TODO(j.swannack): account for ironmen / other account types
    # Initialize user object, if no account type is specified, we assume 'N'
    user = Hiscores(quote(username), "N")

    skills = {
        skill_name: StatInfo(**skill_data)
        for skill_name, skill_data in user.stats.items()
    }

    boss_data = user.data[-(len(boss_list) * 2 + 1) :]

    bosses = {
        boss_name: BossInfo(
            rank=int(boss_data[i * 2]),
            kills=int(boss_data[i * 2 + 1]),
        )
        for i, boss_name in enumerate(boss_list)
        if boss_data[i * 2] != "-1"
    }

    return UserHiscoresInfo(
        username=username,
        timestamp=time.time(),
        skills=skills,
        bosses=bosses,
    )


def load_user_hiscores(
    user_hiscores_info: UserHiscoresInfo, raw_db_client: RawDbClient
):
    raw_db_client.get_hiscores_collection().insert_one(user_hiscores_info.dict())
