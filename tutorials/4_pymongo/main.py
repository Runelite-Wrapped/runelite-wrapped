# Scratch pad when working on this tutorial:
# https://pymongo.readthedocs.io/en/stable/tutorial.html

from pymongo import MongoClient
from bson.objectid import ObjectId
import pymongo
import datetime
import pprint
import os

URI = os.environ["MONGO_URI"]

client = MongoClient(URI)
db = client.get_database("runelite-wrapped-raw")
posts = db.get_collection("posts")

post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow(),
}

post_id = posts.insert_one(post).inserted_id
db.list_collection_names()


pprint.pprint(posts.find_one({"author": "Mike"}))


# The web framework gets post_id from the URL and passes it as a string
def get(post_id):
    # Convert from string to ObjectId:
    return posts.find_one({"_id": ObjectId(post_id)})


new_posts = [
    {
        "author": "Mike",
        "text": "Another post!",
        "tags": ["bulk", "insert"],
        "date": datetime.datetime(2009, 11, 12, 11, 14),
    },
    {
        "author": "Eliot",
        "title": "MongoDB is fun",
        "text": "and pretty easy too!",
        "date": datetime.datetime(2009, 11, 10, 10, 45),
    },
]
result = posts.insert_many(new_posts)

for post in posts.find({"author": "Mike"}):
    pprint.pprint(post)

for post in posts.find():
    pprint.pprint(post)

d = datetime.datetime(2009, 11, 12, 12)
for post in posts.find({"date": {"$lt": d}}).sort("author"):
    pprint.pprint(post)
