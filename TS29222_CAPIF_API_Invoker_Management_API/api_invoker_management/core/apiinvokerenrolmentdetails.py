import pymongo
import secrets
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder


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

    res = mycol.find({'$or': [{'onboarding_information.api_invoker_certificate': apiinvokerenrolmentdetail.onboarding_information.api_invoker_certificate},
                                    {'onboarding_information.api_invoker_public_key': apiinvokerenrolmentdetail.onboarding_information.api_invoker_public_key},
                                    {'onboarding_information.onboarding_secret': apiinvokerenrolmentdetail.onboarding_information.onboarding_secret},
                                    {'notification_destination': apiinvokerenrolmentdetail.notification_destination}
                                    ]})
    if res.count() != 0:
        myclient.close()
        return Response("The CAPIF core has accepted the Onboarding request and is processing it.", status=202, mimetype='application/json')
    else:
        apiinvokerenrolmentdetail.api_invoker_id = secrets.token_hex(15)
        mycol.insert_one(apiinvokerenrolmentdetail.to_dict())
        myclient.close()
        res = Response(json.dumps(apiinvokerenrolmentdetail, cls=JSONEncoder), status=200, mimetype='application/json')
        res.headers['Location'] = "http://localhost:8080/api-invoker-management/v1/onboardedInvokers/" + apiinvokerenrolmentdetail.api_invoker_id
        return res

