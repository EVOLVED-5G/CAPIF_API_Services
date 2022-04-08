import sys

import pymongo
import secrets
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails


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

    res = mycol.find_one({'onboarding_information.api_invoker_public_key': apiinvokerenrolmentdetail.onboarding_information.api_invoker_public_key})

    if res is not None:
        myclient.close()
        prob = ProblemDetails(title="Forbidden", status=403, detail="Invoker already registered", cause="Identical invoker public key")
        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')
    else:

        import requests

        url = "http://easy_rsa:8080/sign-csr"

        payload = dict()
        payload['csr'] = apiinvokerenrolmentdetail.onboarding_information.api_invoker_public_key
        payload['mode'] = 'client'
        payload['filename'] = apiinvokerenrolmentdetail.api_invoker_information

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        sys.stdout.flush()
        response_payload = json.loads(response.text)

        api_invoker_id = secrets.token_hex(15)
        apiinvokerenrolmentdetail.api_invoker_id = api_invoker_id
        apiinvokerenrolmentdetail.onboarding_information.api_invoker_certificate = response_payload['certificate']
        mycol.insert_one(apiinvokerenrolmentdetail.to_dict())
        myclient.close()
        res = Response(json.dumps(apiinvokerenrolmentdetail, cls=JSONEncoder), status=201, mimetype='application/json')
        res.headers['Location'] = "http://localhost:8080/api-invoker-management/v1/onboardedInvokers/" + str(api_invoker_id)
        return res


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

        if old_values is None:
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

