import os
from pymongo import MongoClient

from ImageSoup import ElsevierImageSoup

'''
Failed for the following:
10.1016/j.ssc.2010.05.009
10.1016/j.optcom.2015.07.032
10.1016/j.bioelechem.2009.06.002
TODO(aksub99): investigate reasons for failures.
'''

client = MongoClient()
db = client['AuNP']
collection = db.Paper_Raw_HTML

image_collection = db.Image_Meta

for doc in collection.find({'Publisher': "Elsevier"}):
    meta = {}
    content = doc["Paper_Raw_HTML"]

    try:
        figures = ElsevierImageSoup.parse(content)
    except:
        print("No figures in paper!")
        print("doi", doc["DOI"])
        continue

    meta["DOI"] = doc["DOI"]
    meta["Publisher"] = doc["Publisher"]
    meta["Figures"] = figures["figures"]

    if image_collection.find_one({"DOI": meta["DOI"]}) is None:
        image_collection.insert_one(meta)
