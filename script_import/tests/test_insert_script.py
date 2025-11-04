import os
import pandas as pd
from pymongo import MongoClient
import csv_info
import db_info        

csv_path = 'data/healthcare_dataset.csv'
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

def test_type_columns():
    assert db_info.get_type_columns_db(collection) == {'_id', 'Name', 'Age', 'Gender', 'Blood_Type', 'Insurance_Provider', 'Admission', 'Diagnostic'}, 'Types des champs incorrect!'  

def test_admission_type():
    assert db_info.get_type_admission_db(collection) == ['Elective','Emergency','Urgent'], 'Type de Admissions non reconnus'

def test_range_age():
    min_age, max_age = db_info.get_range_age_db(collection)
    assert min_age["Age"] >= 0 , 'Age négatif?'  
    assert max_age["Age"] <= 120, 'Age trop élevé: ' + str(max_age["Age"])