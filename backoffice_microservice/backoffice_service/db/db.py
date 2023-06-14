from pymongo import MongoClient
from ..config import Config


class MongoDatabse():

    def __init__(self):
        self.config = Config().get_config()
        self.db = self.__connect()
        self.invokers = self.config['mongo']['col_invoker']
        self.providers = self.config['mongo']['col_provider']
        self.services = self.config['mongo']['col_services']
        self.security_context = self.config['mongo']['col_security']
        self.events = self.config['mongo']['col_event']


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
