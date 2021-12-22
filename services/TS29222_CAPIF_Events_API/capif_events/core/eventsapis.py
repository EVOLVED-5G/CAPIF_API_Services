import sys

import pymongo
import secrets
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from bson import json_util


def post_event(subscriber_id, event_subscription):


    ##Conection database
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


    ##Generate subscriptionID
    subscription_id= secrets.token_hex(15)
    print(subscription_id)
    evnt = dict()
    evnt ["subscriber_id"] = subscriber_id
    evnt ["subscription_id"] = subscription_id
    evnt.update(event_subscription.to_dict())
    mycol.insert_one(evnt)
    myclient.close()
    
    res = Response(json.dumps(event_subscription, cls=JSONEncoder), status=201, mimetype='application/json')
    res.headers['Location'] = "http://localhost:8080/capif-events/v1/" + str(subscriber_id) + "/subscriptions/" + str(subscription_id)
    return res




def delete_event(subscriber_id, subscription_id):


    ##Conection database
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    jwt = current_app.config['MONGODB_SETTINGS']['jwt']
    col = current_app.config['MONGODB_SETTINGS']['col']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    mycol = mydb[col]


    myQuery = {'subscriber_id': subscriber_id, 'subscription_id': subscription_id}
    eventdescription = mycol.find_one(myQuery)

    print(eventdescription)

    if eventdescription is None:
        print("hola")
        myclient.close()
        prob = ProblemDetails(title="Not Found", status=404, detail="Service API not existing",
                                cause="Event API subscription id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype='application/json')
    else:
        mycol.delete_one(myQuery)
        return Response(json.dumps(eventdescription, default=str, cls=JSONEncoder), status=204, mimetype='application/json')
 