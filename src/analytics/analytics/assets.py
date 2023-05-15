from dagster import asset


from analytics.tick_count import main


# TODO(j.swannack): resource for mongo client
@asset
def tick_count():
    return main()
