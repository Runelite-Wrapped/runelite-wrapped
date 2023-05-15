from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    DefaultScheduleStatus,
    define_asset_job,
    load_assets_from_modules,
)

from . import assets

all_assets = load_assets_from_modules([assets])

hackernews_job = define_asset_job("hackernew_job", selection=AssetSelection.all())

hackernews_shcedule = ScheduleDefinition(
    job=hackernews_job,
    cron_schedule="0 * * * *",
    default_status=DefaultScheduleStatus.RUNNING,
)

defs = Definitions(
    assets=all_assets,
    jobs=[hackernews_job],
    schedules=[hackernews_shcedule],
)
