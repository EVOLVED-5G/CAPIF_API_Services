import pymongo
import secrets
from flask import current_app, Flask


def add_apiinvokerenrolmentdetail(apiinvokerenrolmentdetail):

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

    apiinvokerenrolmentdetail._api_invoker_id = secrets.token_hex(15)

    try:
        mycol.insert_one(apiinvokerenrolmentdetail.to_dict())
    except Exception:
        return 'bad request!', 400
    finally:
        myclient.close()
        return apiinvokerenrolmentdetail, 200

def update_apiinvokerenrolmentdetail(onboard_id, apiinvokerenrolmentdetail):

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

    apiinvokerenrolmentdetail.api_list.api_name = "Industry 4.0"

    try:
        myQuery = {'api_invoker_id':onboard_id}
        old_values = mycol.find(myQuery)
        print(old_values)
        mycol.update_one(old_values, apiinvokerenrolmentdetail.to_dict())
    except Exception:
        return 'bad request!', 400
    finally:
        myclient.close()
        return apiinvokerenrolmentdetail, 200

def remove_apiinvokerenrolmentdetail(onboard_id):

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



    try:
        myQuery ={'api_invoker_id':onboard_id}
        mycol.delete_one(myQuery)
    except Exception:
        return "This ID is not a registered NetAPP" + onboard_id, 400
    finally:
        myclient.close()
        return " NetAPP with ID " + onboard_id + " has been deleted",200
