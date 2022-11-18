from pymongo import MongoClient
from .config import Config
from elasticsearch import Elasticsearch


class MongoDatabse():

    def __init__(self):
        self.config = Config().getConfig()
        self.db = self.__connect()
        self.invocation_logs = self.config['mongo']['col']
        self.invoker_details = self.config['mongo']['col2']
        self.provider_details = self.config['mongo']['col3']
        self.capif_users = self.config['mongo']['capif_users_col']

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


class ELKDatabase():

    def __init__(self):
        self.db = self.__connect()

    def get_connector(self):
        return self.db

    def __connect(self):

        es = Elasticsearch(
            hosts=['http://elasticsearch:9200'],
            basic_auth=('elastic', 'changeme'),
            retry_on_timeout=True
        )

        return es
