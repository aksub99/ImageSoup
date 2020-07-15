import os
from pymongo import MongoClient

from ImageSoup import SpringerImageSoup

'''
Failure DOIs:
10.1007/s11244-018-0920-7
10.1007/s10562-018-2389-1
10.1007/s10562-014-1255-z
10.1007/s10562-017-2231-1
10.1007/s10800-013-0589-3
10.1007/s11244-013-0154-7
10.1007/s10562-017-2245-8

TODO(aksub99): Investigate reasons for failures.
'''

client = MongoClient()
db = client['AuNP']
collection = db.Paper_Raw_HTML

image_collection = db.Image_Meta

for doc in collection.find({'Publisher': "Springer"}):
    meta = {}
    content = doc["Paper_Raw_HTML"]

    try:
        figures = SpringerImageSoup.parse(content)
    except:
        print("No figures in paper!")
        print("doi", doc["DOI"])
        continue

    meta["DOI"] = doc["DOI"]
    meta["Publisher"] = doc["Publisher"]
    meta["Figures"] = figures["figures"]

    if image_collection.find_one({"DOI": meta["DOI"]}) is None:
        image_collection.insert_one(meta)
