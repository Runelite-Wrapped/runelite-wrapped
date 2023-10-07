from typing import List
import time
from models.hiscores import UserHiscoresInfo, BossInfo
from models.analytics import UserHiscoresGains, BossGains, SkillGains

from analytics.mongo import RawDbClient, AnalyticsDbClient


def calculate_user_hiscores_gains(
    username: str,
    boss_list: List[str],
    raw_db_client: RawDbClient,
) -> UserHiscoresGains:
    """Calculate the stat gains of a user.

    Args:
        username (str): The username of the user.
        raw_db_client (RawDbClient): The raw database client.
    """

    # Get the latest hiscores for the user.
    cursor = raw_db_client.get_hiscores_collection().find(
        {"username": username},
        sort=[("timestamp", -1)],
    )
    hiscores: List[UserHiscoresInfo] = [
        UserHiscoresInfo(**hiscores) for hiscores in cursor
    ]
    output = UserHiscoresGains(
        timestamp=time.time(),
        username=username,
        boss_gains=BossGains(timestamps=[], boss_counts={}, boss_ranks={}),
        skill_gains=SkillGains(timestamps=[], experience_gains={}),
    )

    for hiscores_scrape in hiscores:
        timestamp = hiscores_scrape.timestamp

        output.boss_gains.timestamps.append(timestamp)
        output.skill_gains.timestamps.append(timestamp)

        # Boss gains
        for boss_name in boss_list:
            boss_info = hiscores_scrape.bosses.get(boss_name)
            if boss_info is None:
                boss_info = BossInfo(rank=-1, kills=-1)

            # kill count
            if boss_name not in output.boss_gains.boss_counts:
                output.boss_gains.boss_counts[boss_name] = []

            output.boss_gains.boss_counts[boss_name].append(boss_info.kills)

            # rank
            if boss_name not in output.boss_gains.boss_ranks:
                output.boss_gains.boss_ranks[boss_name] = []

            output.boss_gains.boss_ranks[boss_name].append(boss_info.rank)

        # Skill gains
        for skill_name, skill_info in hiscores_scrape.skills.items():
            # experience
            if skill_name not in output.skill_gains.experience_gains:
                output.skill_gains.experience_gains[skill_name] = []

            output.skill_gains.experience_gains[skill_name].append(
                skill_info.experience
            )

    return output


def load_user_hiscores_gains(
    user_hiscores_gains: UserHiscoresGains,
    analytics_db_client: AnalyticsDbClient,
):
    analytics_db_client.get_hiscores_gains_collection().insert_one(
        user_hiscores_gains.dict()
    )
