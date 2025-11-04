from pymongo import MongoClient

def get_nbrline_db(coll_name):

    MONGO_HOST = "mongodb"
    MONGO_PORT = 27017
    MONGO_DB = "hcare_db"
    uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    mongoClient = MongoClient(uri)
    db = mongoClient[MONGO_DB]
    collection = db[coll_name]

    return collection.count_documents({})