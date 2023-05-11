import requests
from dagster import asset  # import the `dagster` library


@asset  # add the asset decorator to tell Dagster this is an asset
def topstory_ids():
    newstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    top_new_story_ids = requests.get(newstories_url).json()[:100]
    return top_new_story_ids
