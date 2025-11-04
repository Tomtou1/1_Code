from pymongo import MongoClient
import pandas as pd

def get_nbrline_db(collection):
    return collection.count_documents({})

def get_nbrcolumns_db(collection):
    dfbdd = pd.DataFrame(list(collection.find({}, projection={"_id": 0})))
    return dfbdd.shape[1]

def get_doublons_db(collection):
    dfbdd = pd.DataFrame(list(collection.find({}, projection={"_id": 0})))
    return dfbdd.duplicated().sum()

def get_missing_data_db(collection):
    dfbdd = pd.DataFrame(list(collection.find({}, projection={"_id": 0})))
    return sum(dfbdd.isna().sum())