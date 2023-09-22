from dagster import asset, get_dagster_logger

from analytics.extract.items import get_osrsbox_db
from models.items import OsrsItemDb

from analytics.processing.tick_count import (
    calculate_all_user_tick_counts,
    load_all_user_tick_counts,
)
from analytics.mongo import RawDbClient, AnalyticsDbClient

_logger = get_dagster_logger(__name__)


@asset
def tick_count():
    # TODO(j.swannack): make these dagster resources
    raw_db_client = RawDbClient()
    analytics_db_client = AnalyticsDbClient()

    tick_counts = calculate_all_user_tick_counts(raw_db_client=raw_db_client)
    _logger.info(f"Calculated tick counts for {len(tick_counts)} users")
    load_all_user_tick_counts(tick_counts, analytics_db_client=analytics_db_client)
    _logger.info(f"Loaded tick counts for {len(tick_counts)} users")


@asset()
def osrs_item_db() -> OsrsItemDb:
    return get_osrsbox_db()
