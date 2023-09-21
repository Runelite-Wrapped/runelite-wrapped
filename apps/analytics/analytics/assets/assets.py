from dagster import asset, get_dagster_logger

from analytics.tick_count import (
    calculate_all_user_tick_counts,
    load_all_user_tick_counts,
)

logger = get_dagster_logger(__name__)


@asset
def tick_count():
    tick_counts = calculate_all_user_tick_counts()
    load_all_user_tick_counts(tick_counts)


@asset
def hey(tick_count: dict):
    logger.info("hey this is the pipeline running")
    logger.info("goodbye")
    logger.info(tick_count)
    print("hey")
