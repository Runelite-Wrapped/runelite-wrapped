import time

from models.telemetry import ActorDeathEvent
from models.analytics import UserDeathStats, UserDeath, AnalyticsLocationData

from models.regions import get_location_name

from analytics.mongo import RawDbClient, AnalyticsDbClient


def calculate_user_actor_death_stats(
    username: str,
    raw_db_client: RawDbClient,
) -> None:
    raw_deaths = raw_db_client.get_actor_death_collection().find(
        {
            "username": username,
            "data.name": username,
        }
    )
    raw_deaths = [ActorDeathEvent(**death) for death in raw_deaths]

    return UserDeathStats(
        timestamp=time.time(),
        username=username,
        value=[
            UserDeath(
                timestamp=death.timestamp,
                location_data=AnalyticsLocationData(
                    **death.data.location.dict(),
                    name=get_location_name(death.data.location.regionId)
                ),
            )
            for death in raw_deaths
        ],
    )


def load_user_actor_death_stats(
    user_death_stats: UserDeathStats,
    analytics_db_client: AnalyticsDbClient,
) -> None:
    analytics_db_client.get_user_death_collection().insert_one(user_death_stats.dict())
