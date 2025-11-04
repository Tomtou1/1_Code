from datetime import datetime
import os
import time
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
    header = ['Name','Age','Gender','Blood Type','Medical Condition','Date of Admission','Doctor','Hospital','Insurance Provider','Billing Amount','Room Number','Admission Type','Discharge Date','Medication','Test Results']
    reader = df.to_dict(orient="records")

    #Insertion des informations
    documents = []
    for _, row in df.iterrows():
        doc = {
        "Name": row["Name"],
        "Age": int(row["Age"]),
        "Gender": row["Gender"],
        "Blood_Type": row["Blood Type"],
        "Insurance_Provider": row["Insurance Provider"],
        "Admission": {
            "Date_of_Admission": datetime.strptime(row["Date of Admission"], "%Y-%m-%d"),
            "Discharge_Date": datetime.strptime(row["Discharge Date"], "%Y-%m-%d"),
            "Admission_Type": row["Admission Type"],
            "Hospital": row["Hospital"],
            "Room_Number": row["Room Number"],
            "Doctor": row["Doctor"],
            "Billing_Amount": float(row["Billing Amount"]),
            "Doctor": row["Doctor"],
        },
        "Diagnostic": {
            "Medical_Condition": row["Medical Condition"],
            "Medication": row["Medication"],
            "Test_Results": row["Test Results"]
        },
        }
        documents.append(doc)



# --- Insertion dans MongoDB ---
    if documents:
        collection.insert_many(documents)
        print(f"{len(documents)} documents insérés dans la collection 'patients'")

        fields = set()
        for doc in collection.find():
            fields.update(doc.keys())

        print(fields)