from pymongo import MongoClient
from ..config import Config
from bson.codec_options import CodecOptions


class MongoDatabse():

    def __init__(self):
        self.config = Config().getConfig()
        self.db = self.__connect()
        self.provider_enrolment_details = self.config['mongo']['col']
        self.capif_users = self.config['mongo']['capif_users']

    def get_col_by_name(self, name):
        return self.db[name].with_options(codec_options=CodecOptions(tz_aware=True))

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


