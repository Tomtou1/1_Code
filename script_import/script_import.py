import pandas as pd
from pymongo import MongoClient

#Lecture du CSV
df = pd.read_csv("script_import/data/hcare_dataset_test.csv")
print(f"CSV file has {df.shape[0]} rows.")


MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "hcare_db"

uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
client = MongoClient(uri)  # Création d'un nouveau client et connection au serveur
    
try:
    client.admin.command("ping")  
    print("Connection établie - MongoDB!")
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