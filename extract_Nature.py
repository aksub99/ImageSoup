import os
from pymongo import MongoClient

from ImageSoup import NatureImageSoup

# TODO(aksub99): Fix nature nanotechnology (dois are like 10.1038/nnano.2015.33)

client = MongoClient()
db = client['AuNP']
collection = db.Paper_Raw_HTML

image_collection = db.Image_Meta

for doc in collection.find({'Publisher': "Nature Publishing Group"}):
    meta = {}
    content = doc["Paper_Raw_HTML"]

    try:
        figures = NatureImageSoup.parse(content, doi=doc["DOI"])
        if figures["figures"] == []:
            continue
    except:
        print("No figures in paper!")
        print(doc["DOI"])
        continue

    meta["DOI"] = doc["DOI"]
    meta["Publisher"] = doc["Publisher"]
    meta["Figures"] = figures["figures"]

    if image_collection.find_one({"DOI": meta["DOI"]}) is None:
        image_collection.insert_one(meta)
