from dagster import EnvVar, ConfigurableResource
from analytics.mongo import RawDbClient, AnalyticsDbClient


class MongoClient(ConfigurableResource):
    uri: str

    def get_raw_client(self) -> RawDbClient:
        return RawDbClient(uri=self.uri)

    def get_analytics_client(self) -> AnalyticsDbClient:
        return AnalyticsDbClient(uri=self.uri)


RESOURCES = {
    "mongo_client": MongoClient(uri=EnvVar("MONGO_URI")),
}
