import pymongo
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from bson import json_util


def get_discoveredapis(api_invoker_id, api_name=None, api_version=None, comm_type=None, protocol=None, aef_id=None,
                       data_format=None, api_cat=None, supported_features=None, api_supported_features=None):

    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    serv = current_app.config['MONGODB_SETTINGS']['services']
    inv = current_app.config['MONGODB_SETTINGS']['invokers']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    services = mydb[serv]
    invokers = mydb[inv]

    invoker = invokers.find_one({"api_invoker_id": api_invoker_id})
    if invoker is None:
        myclient.close()
        prob = ProblemDetails(title="Forbidden", status=403, detail="API Invoker does not exist", cause="API Invoker id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')
    else:
        myParams = []
        myQuery = {}
        if api_name is not None:
            myParams.append({"api_name": api_name})
        if api_version is not None:
            myParams.append({"aef_profiles.0.versions.api_version": api_version})
        if comm_type is not None:
            myParams.append({"aef_profiles.0.versions.resources.comm_type": comm_type})
        if protocol is not None:
            myParams.append({"aef_profiles.0.protocol": protocol})
        if aef_id is not None:
            myParams.append({"aef_profiles.0.aef_id": aef_id})
        if data_format is not None:
            myParams.append({"aef_profiles.0.data_format": data_format})
        if api_cat is not None:
            myParams.append({"service_api_category": api_cat})
        if supported_features is not None:
            myParams.append({"supported_features": supported_features})
        if api_supported_features is not None:
            myParams.append({"api_supp_feats": api_supported_features})
        if myParams:
            myQuery = {"$or": myParams}
        discoved_apis = services.find(myQuery)
        json_docs = []
        for discoved_api in discoved_apis:
            del discoved_api['_id']
            del discoved_api['apf_id']
            json_doc = json.dumps(discoved_api, default=json_util.default)
            json_docs.append(json_doc)

        myclient.close()
        res = Response(json_docs, status=200, mimetype='application/json')
        return res
