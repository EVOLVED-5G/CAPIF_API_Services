import pymongo
import secrets
from flask import current_app, Flask


def get_discoveredapis(api_invoker_id):

    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    col = current_app.config['MONGODB_SETTINGS']['col']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    mycol = mydb[col]

    discoved_apis = {}
    try:
        discoved_apis = mycol.find_one({"_id": api_invoker_id})
    except KeyError:
        return {}, 404
    finally:
        myclient.close()
        return discoved_apis, 200
