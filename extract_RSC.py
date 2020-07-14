import os
from pymongo import MongoClient

from ImageSoup import RSCImageSoup


client = MongoClient()
db = client['AuNP']
collection = db.Paper_Raw_HTML

image_collection = db.Image_Meta

for doc in collection.find({'Publisher': "The Royal Society of Chemistry"}):
    meta = {}
    content = doc["Paper_Raw_HTML"]

    try:
        figures = RSCImageSoup.parse(content)
    except:
        print("No figures in paper!")
        continue

    meta["DOI"] = doc["DOI"]
    meta["Publisher"] = doc["Publisher"]
    meta["Figures"] = figures["figures"]

    if image_collection.find_one({"DOI": meta["DOI"]}) is None:
        image_collection.insert_one(meta)
