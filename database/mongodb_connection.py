from pymongo import MongoClient
import pymongo




def create_mongo_client():
    var_url = f"mongodb+srv://joeysabusido:genesis11@cluster0.bmdqy.mongodb.net/ldglobal?retryWrites=true&w=majority"
    client = MongoClient(var_url, maxPoolSize=None)
    conn = client['accounting_database']

    return conn