import atexit
import time
from pymongo import MongoClient
from pymongo.errors import AutoReconnect
from ..config import Config
from bson.codec_options import CodecOptions
import os
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor

if eval(os.environ.get("MONITORING").lower().capitalize()):
    PymongoInstrumentor().instrument()


class MongoDatabse():

    def __init__(self):
        self.config = Config().get_config()
        self.db = self.__connect()
        self.invocation_logs = self.config['mongo']['logs_col']
        self.invoker_details = self.config['mongo']['invoker_col']
        self.provider_details = self.config['mongo']['prov_col']
        self.service_apis = self.config['mongo']['serv_col']
        self.capif_users = self.config['mongo']['capif_users_col']

    def get_col_by_name(self, name):
        return self.db[name]

    def __connect(self, max_retries=3, retry_delay=1):
        retries = 0
        while retries < max_retries:
            try:
                uri = f"mongodb://{self.config['mongo']['user']}:{self.config['mongo']['password']}@" \
                      f"{self.config['mongo']['host']}:{self.config['mongo']['port']}"
                client = MongoClient(uri)
                mydb = client[self.config['mongo']['db']]
                mydb.command("ping")
                return mydb
            except AutoReconnect:
                retries += 1
                print(f"Reconnecting... Retry {retries} of {max_retries}")
                time.sleep(retry_delay)
        return None

    def close_connection(self):
        if self.db.client:
            self.db.client.close()
