from dagster import asset, get_dagster_logger

from analytics.processing.tick_count import (
    calculate_all_user_tick_counts,
    load_all_user_tick_counts,
)

_logger = get_dagster_logger(__name__)


@asset
def tick_count():
    tick_counts = calculate_all_user_tick_counts()
    _logger.info(f"Calculated tick counts for {len(tick_counts)} users")
    load_all_user_tick_counts(tick_counts)
    _logger.info(f"Loaded tick counts for {len(tick_counts)} users")
