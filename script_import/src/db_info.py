from pymongo import MongoClient

def get_nbrline_db(mongoClient,db_name, coll_name):

    db = mongoClient[db_name]
    collection = db[coll_name]

    return collection.count_documents({})
