import os
import pandas as pd
from pymongo import MongoClient
import csv_info
import db_info        

csv_path = 'data/hcare_dataset_test.csv'
collection_name = 'traitement' 

MONGO_HOST = os.environ.get("MONGO_HOST", "mongodb")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_DB = os.environ.get("MONGO_DB", "hcare_db")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")
MONGO_COLLECTION = "traitement"

uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"

mongoClient = MongoClient(uri)
db = mongoClient[MONGO_DB]
collection = db[MONGO_COLLECTION]

def test_count_lines():    
    assert csv_info.get_nbrline_csv(csv_path) == db_info.get_nbrline_db(collection), 'Nbre ligne incorrect: '  + str(csv_info.get_nbrline_csv(csv_path)) + ' dans le csv et ' + str(db_info.get_nbrline_db(collection)) + ' dans la bdd'  

def test_count_columns():
    assert csv_info.get_nbrcolumns_csv(csv_path) == db_info.get_nbrcolumns_db(collection), 'Nbre colonnes incorrect: ' + str(csv_info.get_nbrcolumns_csv(csv_path)) + ' dans le csv et ' + str(db_info.get_nbrcolumns_db(collection)) + ' dans la bdd'  

def test_count_doublons():
    assert csv_info.get_doublons_csv(csv_path) == db_info.get_doublons_db(collection), 'Nbre doublons incorrect: ' + str(csv_info.get_doublons_csv(csv_path)) + ' dans le csv et ' + str(db_info.get_doublons_db(collection)) + ' dans la bdd'  

def test_count_missingdata():
    assert csv_info.get_missing_data_csv(csv_path) == db_info.get_missing_data_db(collection), 'Nbre données manquantes incorrect: ' + str(csv_info.get_missing_data_csv(csv_path)) + ' dans le csv et ' + str(db_info.get_missing_data_db(collection)) + ' dans la bdd'  