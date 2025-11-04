import pandas as pd
from pymongo import MongoClient
import csv_info
import db_info        

csv_path = 'data/hcare_dataset_test.csv'
collection_name = 'traitement' 

def test_count_lines():
    
    assert csv_info.get_nbrline_csv(csv_path) == db_info.get_nbrline_db(collection_name), 'Nbre ligne incorrect: '  + str(csv_info.get_nbrline_csv(csv_path)) + ' dans le csv et ' + str(db_info.get_nbrline_db(bdd_name,collection_name)) + ' dans la bdd'  
