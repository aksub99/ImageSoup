import pymongo
from pymongo import MongoClient


client_AuNP = MongoClient(port=27017)
db_AuNP = client_AuNP["AuNP"]
collection_AuNP = db_AuNP.Paper_Metadata

def get_year(doi):
    year = collection_AuNP.find_one({"DOI": doi})["Published_Year"]
    return year