from dagster_duckdb_pandas import DuckDBPandasIOManager
from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    DefaultScheduleStatus,
    define_asset_job,
    load_assets_from_modules,
    FilesystemIOManager,
)

from . import assets

all_assets = load_assets_from_modules([assets])

hackernews_job = define_asset_job("hackernew_job", selection=AssetSelection.all())

hackernews_schedule = ScheduleDefinition(
    job=hackernews_job,
    cron_schedule="0 * * * *",
    default_status=DefaultScheduleStatus.RUNNING,
)

io_manager = FilesystemIOManager(base_dir="data")
database_io_manager = DuckDBPandasIOManager(database="data/analytics.hackernews")

defs = Definitions(
    assets=all_assets,
    jobs=[hackernews_job],
    schedules=[hackernews_schedule],
    resources={
        "io_manager": io_manager,
        "database_io_manager": database_io_manager,
    },
)
