from pymongo import MongoClient
from .config import Config


class MongoDatabse():

    def __init__(self):
        self.config = Config().getConfig()
        self.db, self.db_capif = self.__connect()
        self.capif_users = self.config['mongo']['col']


    def get_col_by_name(self, name):
        if name != "user":
            return self.db_capif[name]
        return self.db[name]

    def __connect(self):
        uri = "mongodb://" + self.config['mongo']['user'] + ":" + self.config['mongo']['password'] + "@" + self.config['mongo']['host'] + ":" + self.config['mongo']['port']
        client = MongoClient(uri)

        try:
            client.admin.command("ping")
            mydb = client[self.config['mongo']['db']]
            mydb_capif =client[self.config['mongo']['db_capif']]
            return mydb, mydb_capif
        except Exception as e:
            print("An exception occurred ::", e)
            return None
