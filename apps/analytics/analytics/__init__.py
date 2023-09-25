from dagster import Definitions, load_assets_from_modules

from analytics.assets import assets
from analytics.resources import RESOURCES

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    resources=RESOURCES,
)
