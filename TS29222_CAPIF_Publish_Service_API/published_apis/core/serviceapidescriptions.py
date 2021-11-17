import pymongo
import secrets
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails


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
        res = mycol.find({'api_name': serviceapidescription.api_name})
        if res.count() != 0:
            myclient.close()
            prob = ProblemDetails(title="Forbidden", status=403, detail="Service already published",
                                  cause="Identical API name")
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
