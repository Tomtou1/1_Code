import os
import time
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


MONGO_HOST = os.environ.get("MONGO_HOST", "mongodb")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_DB = os.environ.get("MONGO_DB", "hcare_db")


uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"

for _ in range(10):
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print("Connexion à Mongo réussie !")
        break
    except ServerSelectionTimeoutError:
        print("Mongo pas encore prêt, retry dans 3s...")
        time.sleep(3)

#Lecture du CSV
df = pd.read_csv("data/hcare_dataset_test.csv")
print(f"CSV file has {df.shape[0]} rows.")

    
try:
    db = client[MONGO_DB]
    collection = db['traitement'] # Création DB traitement
    
    collection.delete_many({}) # pour le dev, à commenter plus tard
    #Verification que la collection est vide
    nb_docs = collection.count_documents({})
    print(f"Avant insertion, la collection contient {nb_docs} documents 📦")

    #Création des headers
    header = ['Name','Age','Gender']
    reader = df.to_dict(orient="records")

    #Insertion
    for each in reader:
        row = {}
        for field in header:
            row[field] = each[field]
        collection.insert_one(row)

    #Vérification du nbre de docs après insertion
    nb_docs = collection.count_documents({})
    print(f"Après insertion, la collection contient {nb_docs} documents 📦")

except Exception as e:
    print(e)