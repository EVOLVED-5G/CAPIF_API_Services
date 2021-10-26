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

    res = mycol.find({'onboarding_information.api_invoker_public_key': apiinvokerenrolmentdetail.onboarding_information.api_invoker_public_key})

    if res.count() != 0:
        myclient.close()
        prob = ProblemDetails(title="Forbidden", status=403, detail="Invoker already registered", cause="Identical invoker public key")
        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')
    else:
        apiinvokerenrolmentdetail.api_invoker_id = secrets.token_hex(15)
        _id = mycol.insert_one(apiinvokerenrolmentdetail.to_dict())
        myclient.close()
        res = Response(json.dumps(apiinvokerenrolmentdetail, cls=JSONEncoder), status=201, mimetype='application/json')
        res.headers['Location'] = "http://localhost:8080/api-invoker-management/v1/onboardedInvokers/" + str(_id.inserted_id)
        return res

