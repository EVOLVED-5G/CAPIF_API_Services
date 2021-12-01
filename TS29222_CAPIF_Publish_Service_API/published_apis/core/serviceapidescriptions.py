import pymongo
import secrets
from flask import current_app, Flask, Response
import json

from pymongo import response
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from bson import json_util


def get_serviceapis(apf_id):
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    col = current_app.config['MONGODB_SETTINGS']['col']
    jwt = current_app.config['MONGODB_SETTINGS']['jwt']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    mycol = mydb[col]
    user_registry = mydb[jwt]

    apf_res = user_registry.find({'_id': apf_id})
    if apf_res.count() == 0:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="APF not existing",
                              cause="APF id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')
    else:
        myQuery = {'apf_id': apf_id}
        service_apis = mycol.find(myQuery)
        json_docs = []
        for serviceapi in service_apis:
            del serviceapi['apf_id']
            del serviceapi['_id']
            json_docs.append(serviceapi)

        myclient.close()
        res = Response(json.dumps(json_docs, default=json_util.default), status=200, mimetype='application/json')
        return res


def add_serviceapidescription(apf_id, serviceapidescription):
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    col = current_app.config['MONGODB_SETTINGS']['col']
    jwt = current_app.config['MONGODB_SETTINGS']['jwt']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    mycol = mydb[col]
    user_registry = mydb[jwt]

    apf_res = user_registry.find({'_id': apf_id})

    if apf_res.count() == 0:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="APF not existing",
                              cause="APF id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')
    else:
        myParams = [{"api_name": serviceapidescription.api_name}]
        for i in range(0,len(serviceapidescription.aef_profiles)):
            myParams.append({"aef_profiles."+str(i)+".aef_id": serviceapidescription.aef_profiles[i].aef_id})
        myQuery = {"$and": myParams}
        res = mycol.find(myQuery)
        if res.count() != 0:
            myclient.close()
            prob = ProblemDetails(title="Forbidden", status=403, detail="Service already published",
                                  cause="Identical API name and AEF Profile IDs")
            return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')
        else:
            api_id = secrets.token_hex(15)
            serviceapidescription.api_id = api_id
            rec = dict()
            rec['apf_id'] = apf_id
            rec.update(serviceapidescription.to_dict())
            mycol.insert_one(rec)
            myclient.close()
            res = Response(json.dumps(serviceapidescription, cls=JSONEncoder), status=201, mimetype='application/json')
            res.headers['Location'] = "http://localhost:8080/published-apis/v1/" + str(apf_id) + "/service-apis/" + str(api_id)
            return res


def get_one_serviceapi(service_api_id, apf_id):
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    col = current_app.config['MONGODB_SETTINGS']['col']
    jwt = current_app.config['MONGODB_SETTINGS']['jwt']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    mycol = mydb[col]
    user_registry = mydb[jwt]

    apf_res = user_registry.find({'_id': apf_id})
    if apf_res.count() == 0:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="APF not existing",
                              cause="APF id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')
    else:
        myQuery = {'apf_id': apf_id, 'api_id': service_api_id}
        service_api = mycol.find_one(myQuery)
        if service_api is None:
            prob = ProblemDetails(title="Not Found", status=400, detail="Service API not found",
                                  cause="No Service with specific credentials exists")
            return Response(json.dumps(prob, cls=JSONEncoder), status=400, mimetype='application/json')

        del service_api['apf_id']

        myclient.close()
        res = Response(json.dumps(service_api, default=json_util.default), status=200, mimetype='application/json')
        return res

def delete_serviceapidescription(service_api_id, apf_id):
    
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    col = current_app.config['MONGODB_SETTINGS']['col']
    jwt = current_app.config['MONGODB_SETTINGS']['jwt']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']   


    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)

    mydb = myclient[db]
    mycol = mydb[col]
    user_registry = mydb[jwt]

    apf_res = user_registry.find({'_id': apf_id})


    if apf_res.count() == 0:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="APF not existing",
                                cause="APF id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    else:


        myQuery = {'apf_id': apf_id, 'api_id': service_api_id}
        serviceapidescription = mycol.find_one(myQuery)

        if (serviceapidescription == None):
            return "Please provide an existing service api ID", 404
        else:
            mycol.delete_one(myQuery)
         
            return Response(json.dumps(serviceapidescription, default=str, cls=JSONEncoder), status=204, mimetype='application/json')


def update_serviceapidescription(service_api_id,apf_id, service_api_description):

    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    col = current_app.config['MONGODB_SETTINGS']['col']
    jwt = current_app.config['MONGODB_SETTINGS']['jwt']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']   


    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)

    mydb = myclient[db]
    mycol = mydb[col]
    user_registry = mydb[jwt]


    apf_res = user_registry.find({'_id': apf_id})



    if apf_res.count() == 0:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="APF not existing",
                                cause="APF id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    else:

        myQuery = {'apf_id': apf_id, 'api_id': service_api_id}
        serviceapidescription = mycol.find_one(myQuery)


        if (serviceapidescription == None):
            myclient.close()
            return "Please provide an existing service api ID", 404

        else:

            mycol.replace_one(serviceapidescription, service_api_description.to_dict())
            myclient.close()
            response = Response(json.dumps(serviceapidescription, default=str,cls=JSONEncoder), status=201, mimetype='application/json')

            return response
