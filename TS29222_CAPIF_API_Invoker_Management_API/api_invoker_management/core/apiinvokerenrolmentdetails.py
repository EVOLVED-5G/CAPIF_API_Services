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

    apiinvokerenrolmentdetail.api_invoker_id = secrets.token_hex(15)

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

    

    try:
        myQuery = {'api_invoker_id':onboard_id}
        old_values = mycol.find_one(myQuery)
        
        
        if (old_values == None):
            return "Please provide an existing Netapp ID", 404
        else:

            apiinvokerenrolmentdetail.api_invoker_id = onboard_id
            mycol.replace_one(old_values, apiinvokerenrolmentdetail.to_dict())
            return apiinvokerenrolmentdetail, 200
    except Exception:
        return 'bad request!', 400
    finally:
        myclient.close()
        

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
        result=mycol.find_one(myQuery)

        if (result == None):
            return "Please provide an existing Netapp ID", 404
        else:
            mycol.delete_one(myQuery)
            return " The Netapp matching onboardingId  " + onboard_id + " was offboarded.",204
                    
    except Exception:
        return "An error has ocurred with the" + onboard_id, 400
    finally:
        myclient.close()

