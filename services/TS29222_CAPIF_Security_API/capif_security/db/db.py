from pymongo import MongoClient
from .config import Config


class MongoDatabse():

    def __init__(self):
        self.config = Config().getConfig()
        self.db = self.__connect()
        self.security_info = self.config['mongo']['col']
        self.capif_users = self.config['mongo']['capif_users_col']
        self.capif_invokers = self.config['mongo']['capif_invokers']


    def get_col_by_name(self, name):
        return self.db[name]

    def __connect(self):
        uri = "mongodb://" + self.config['mongo']['user'] + ":" + self.config['mongo']['password'] + "@" + self.config['mongo']['host'] + ":" + self.config['mongo']['port']
        client = MongoClient(uri)

        try:
            client.admin.command("ping")
            mydb = client[self.config['mongo']['db']]
            return mydb
        except Exception as e:
            print("An exception occurred ::", e)
            return None
