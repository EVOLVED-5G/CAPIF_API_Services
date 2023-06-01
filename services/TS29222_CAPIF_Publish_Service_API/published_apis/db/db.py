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
        self.service_api_descriptions = self.config['mongo']['col']
        self.capif_provider_col = self.config['mongo']['capif_provider_col']
        self.certs_col = self.config['mongo']['certs_col']


    def get_col_by_name(self, name):
        return self.db[name].with_options(codec_options=CodecOptions(tz_aware=True))

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
