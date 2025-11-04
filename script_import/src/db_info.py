from pymongo import MongoClient
import pandas as pd

def get_nbrline_db(collection):
    return collection.count_documents({})

def get_type_columns_db(collection):
    fields = set()
    for doc in collection.find():
        fields.update(doc.keys())
    return fields

def get_type_admission_db(collection):
    admission_types = collection.distinct("Admission.Admission_Type")
    return admission_types

def get_range_age_db(collection):
    min_age = collection.find_one(sort=[("Age", 1)])
    max_age = collection.find_one(sort=[("Age", -1)])
    return min_age, max_age
