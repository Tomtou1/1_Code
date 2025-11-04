import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

def connection_mongoDB():
    MONGO_HOST = os.environ.get("MONGO_HOST", "mongodb")
    MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
    MONGO_DB = os.environ.get("MONGO_DB", "hcare_db")
    MONGO_USER = os.environ.get("MONGO_USER")
    MONGO_PASS = os.environ.get("MONGO_PASS")

    uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"

    for _ in range(10):
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            client.admin.command('ping')
            print("Connexion à Mongo réussie !")
            break
        except ServerSelectionTimeoutError:
            print("Mongo pas encore prêt, retry dans 3s...")
            time.sleep(3)
    
    return client

def insertion_df_in_coll(df, collection):

    #Création des headers
    header = ['Name','Age','Gender']
    reader = df.to_dict(orient="records")

    #Insertion des informations
    for each in reader:
        row = {}
        for field in header:
            row[field] = each[field]
        collection.insert_one(row)

    print("Insertion finie")