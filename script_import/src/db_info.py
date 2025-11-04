from pymongo import MongoClient
import pandas as pd

def get_nbrline_db(collection):
    return collection.count_documents({})

def get_type_columns_db(collection):
    fields = set()
    for doc in collection.find():
        fields.update(doc.keys())
    return fields

