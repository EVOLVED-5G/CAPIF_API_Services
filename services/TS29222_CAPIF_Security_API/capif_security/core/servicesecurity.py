import sys

import pymongo
import secrets
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from ..models.access_token_rsp import AccessTokenRsp
from bson import json_util
import requests


def get_servicesecurity(api_invoker_id, authentication_info=True, authorization_info=True):
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    serv = current_app.config['MONGODB_SETTINGS']['col']
    inv = current_app.config['MONGODB_SETTINGS']['invokers']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    services_security = mydb[serv]
    invokers = mydb[inv]

    invoker = invokers.find_one({"api_invoker_id": api_invoker_id})
    if invoker is None:
        myclient.close()
        prob = ProblemDetails(title="Forbidden", status=403, detail="API Invoker does not exist",
                              cause="API Invoker id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')
    else:
        myQuery = {'api_invoker_id': api_invoker_id}
        services_security_objects = services_security.find(myQuery)
        json_docs = []
        for services_security_object in services_security_objects:
            del services_security_object['_id']
            del services_security_object['api_invoker_id']
            if not authentication_info:
                for securityInfo_obj in services_security_object['security_info']:
                    del securityInfo_obj['authentication_info']
            if not authorization_info:
                for securityInfo_obj in services_security_object['security_info']:
                    del securityInfo_obj['authorization_info']

            json_doc = json.dumps(services_security_object, default=json_util.default)
            json_docs.append(json_doc)

        myclient.close()
        res = Response(json_docs, status=200, mimetype='application/json')
        return res


def create_servicesecurity(api_invoker_id, service_security):
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    serv = current_app.config['MONGODB_SETTINGS']['col']
    inv = current_app.config['MONGODB_SETTINGS']['invokers']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    services_security = mydb[serv]
    invokers = mydb[inv]

    invoker = invokers.find_one({"api_invoker_id": api_invoker_id})
    if invoker is None:
        myclient.close()
        prob = ProblemDetails(title="Forbidden", status=403, detail="API Invoker does not exist",
                              cause="API Invoker id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')
    else:
        myParams = []
        for i in range(0, len(service_security.security_info)):
            myParams.append({"security_info." + str(i) + ".aef_id": service_security.security_info[i].aef_id})
        myQuery = {"$and": myParams}
        res = services_security.find(myQuery)
        if res.count() != 0:
            myclient.close()
            prob = ProblemDetails(title="Forbidden", status=403, detail="Security method already defined",
                                  cause="Identical AEF Profile IDs")
            return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')
        else:
            rec = dict()
            rec['api_invoker_id'] = api_invoker_id
            rec.update(service_security.to_dict())
            services_security.insert_one(rec)
            myclient.close()
            res = Response(json.dumps(service_security, cls=JSONEncoder), status=201, mimetype='application/json')
            res.headers['Location'] = "http://localhost:8080/capif-security/v1/trustedInvokers/" + str(
                api_invoker_id)
            return res


def delete_servicesecurity(api_invoker_id):
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    serv = current_app.config['MONGODB_SETTINGS']['col']
    inv = current_app.config['MONGODB_SETTINGS']['invokers']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    services_security = mydb[serv]
    invokers = mydb[inv]

    myQuery = {'api_invoker_id': api_invoker_id}
    result = services_security.find(myQuery)
    if result.count() == 0:
        return "Please provide an existing Netapp ID", 404
    else:
        services_security.delete_many(myQuery)
        return "The security info of Netapp with Netapp ID " + api_invoker_id + " were deleted.", 204


def return_token(security_id, access_token_req):
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    serv = current_app.config['MONGODB_SETTINGS']['col']
    inv = current_app.config['MONGODB_SETTINGS']['invokers']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    services_security = mydb[serv]
    invokers = mydb[inv]

    invoker = invokers.find_one({"api_invoker_id": security_id})
    if invoker is None:
        myclient.close()
        prob = ProblemDetails(title="Forbidden", status=403, detail="API Invoker does not exist",
                              cause="API Invoker id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')
    else:
        access_token_url = "http://192.168.1.21:8888/api/v1/login/access-token"
        access_payload = {
            "username": "admin@my-email.com",
            "password": "pass"
        }
        request_token_obj = access_token_req.to_dict()
        # DO NOT REMOVE
        # for (key, value) in request_token_obj.items():
        #     access_payload[key] = value

        response = requests.request('POST', access_token_url, data=access_payload)
        parsed = json.loads(response.text)
        access_token = parsed['access_token']
        token_type = parsed['token_type']
        access_token_resp = AccessTokenRsp(access_token=access_token, token_type=token_type, expires_in=691200)
        if "scope" in request_token_obj.keys():
            access_token_resp.scope = request_token_obj["scope"]
        res = Response(json.dumps(access_token_resp, cls=JSONEncoder), status=201, mimetype='application/json')
        return res


def update_servicesecurity(api_invoker_id, service_security):
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    serv = current_app.config['MONGODB_SETTINGS']['col']
    inv = current_app.config['MONGODB_SETTINGS']['invokers']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    services_security = mydb[serv]
    invokers = mydb[inv]

    invoker = invokers.find_one({"api_invoker_id": api_invoker_id})
    if invoker is None:
        myclient.close()
        prob = ProblemDetails(title="Forbidden", status=403, detail="API Invoker does not exist",
                              cause="API Invoker id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')
    else:
        myParams = []
        for i in range(0, len(service_security.security_info)):
            myParams.append({"security_info." + str(i) + ".aef_id": service_security.security_info[i].aef_id})
        myQuery = {"$and": myParams}
        old_object = services_security.find_one(myQuery)
        if old_object is None:
            myclient.close()
            prob = ProblemDetails(title="Forbidden", status=403, detail="Security context not found",
                                  cause="Not existing AEF Profile IDs")
            return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')
        else:
            new_object = dict()
            new_object['api_invoker_id'] = api_invoker_id
            new_object.update(service_security.to_dict())
            services_security.replace_one(old_object, new_object)
            myclient.close()
            res = Response(json.dumps(service_security, cls=JSONEncoder), status=200, mimetype='application/json')
            res.headers['Location'] = "http://localhost:8080/capif-security/v1/trustedInvokers/" + str(
                api_invoker_id)
            return res


def revoke_api_authorization(api_invoker_id, security_notification):
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    serv = current_app.config['MONGODB_SETTINGS']['col']
    inv = current_app.config['MONGODB_SETTINGS']['invokers']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    services_security = mydb[serv]

    myQuery = {'api_invoker_id': api_invoker_id}
    result = services_security.find(myQuery)
    if result.count() == 0:
        return "Please provide an existing Netapp ID", 404
    else:
        return "Netapp with ID " + api_invoker_id + " was revoked by some APIs.", 204
