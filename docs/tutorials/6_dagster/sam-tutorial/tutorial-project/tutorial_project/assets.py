import pandas as pd  # Add new imports to the top of `assets.py`
import requests

from dagster import asset


@asset  # add the asset decorator to tell Dagster this is an asset
def topstory_ids():
    newstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    top_new_story_ids = requests.get(newstories_url).json()[:100]
    return top_new_story_ids


@asset
def topstories(topstory_ids):  # this asset is dependent on topstory_ids
    results = []
    for item_id in topstory_ids:
        item = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        ).json()
        results.append(item)

        if len(results) % 20 == 0:
            print(f"Got {len(results)} items so far.")  # noqa: T201

    df = pd.DataFrame(results)

    return df
