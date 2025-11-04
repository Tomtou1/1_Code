import os
import time
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from src.script_import_fct import connection_mongoDB,insertion_df_in_coll

#Connection à MongoDB 
client = connection_mongoDB()
    
try:
    #Lecture du csv
    df = pd.read_csv("data/hcare_dataset_test.csv")
    print(f"CSV file has {df.shape[0]} rows.")

    #Creation DB et collection traitement
    db = client['hcare_db']
    collection = db['traitement'] 
    
    collection.delete_many({}) # pour le dev, à commenter plus tard

    #Appel fonction d'insertion du dataframge dans la collection
    insertion_df_in_coll(df, collection)

except Exception as e:
    print(e)