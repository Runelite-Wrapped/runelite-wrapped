from dagster import asset


from analytics.tick_count import calculate_all_user_tick_counts


# TODO(j.swannack): resource for mongo client
@asset
def tick_count():
    return calculate_all_user_tick_counts()
