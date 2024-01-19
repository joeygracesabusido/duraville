from pymongo import MongoClient
import pymongo




def create_mongo_client():
    var_url = f"mongodb+srv://joeysabusido:genesis11@cluster0.bmdqy.mongodb.net/ldglobal?retryWrites=true&w=majority"
    client = MongoClient(var_url, maxPoolSize=None)
    conn = client['accounting_database']

    return conn 


class Connection():

    @staticmethod
    def db(): # this is for connection to Database
        connection_string = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(
            user="joeysabusido",
            password=urllib.parse.quote("Genesis@11"),
            host="192.46.225.247",
            port=3306,
            database="duravileDBl"
        )


        engine = create_engine(connection_string, echo=True)
        return engine
