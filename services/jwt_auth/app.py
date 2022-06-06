#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
import secrets


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'user': 'root',
    'password': 'example',
    'db': 'capif',
    'col': 'invokerdetails',
    'jwt': 'user',
    'host': 'mongo',
    'port': 27017,
}
app.config['CAPIF_HOST'] = {
    'ip': 'localhost',
    'port': 8080,
}

app.config["JWT_SECRET_KEY"] = "this-is-secret-key"

jwt = JWTManager(app)

user = app.config['MONGODB_SETTINGS']['user']
passwd = app.config['MONGODB_SETTINGS']['password']
db = app.config['MONGODB_SETTINGS']['db']
col = app.config['MONGODB_SETTINGS']['jwt']
host = app.config['MONGODB_SETTINGS']['host']
port = app.config['MONGODB_SETTINGS']['port']

capif_ip = app.config['CAPIF_HOST']['ip']
capif_port = app.config['CAPIF_HOST']['port']

uri = "mongodb://" + user + ":" + passwd + "@" + host + ":" + str(port)

myclient = MongoClient(uri)
mydb = myclient[db]
user = mydb[col]
invokerdetails = mydb['invokerdetails']
serviceapidescriptions = mydb['serviceapidescriptions']
eventsdetails = mydb['eventsdetails']
servicesecurity = mydb['servicesecurity']


@app.route("/register", methods=["POST"])
def register():
    username = request.json["username"]
    role = request.json["role"]
    test = user.find_one({"username": username})
    if test:
        return jsonify("User already exists"), 409
    elif role != "invoker" and role != "apf":
        return jsonify(message="Role must be invoker or apf"), 409
    else:
        username = request.json["username"]
        password = request.json["password"]
        role = request.json["role"]
        description = request.json["description"]
        cn = request.json["cn"]
        user_info = dict(_id=secrets.token_hex(7), username=username, password=password, role=role, description=description, cn=cn)
        obj = user.insert_one(user_info)

        if role == "invoker":
            return jsonify(message=role + " registered successfully",
                           id=obj.inserted_id,
                           ccf_onboarding_url="api-invoker-management/v1/onboardedInvokers",
                           ccf_discover_url="service-apis/v1/allServiceAPIs?api-invoker-id="), 201
        elif role == "apf":
            return jsonify(message=role + " registered successfully",
                           id=obj.inserted_id,
                           ccf_publish_url="published-apis/v1/{}/service-apis".format(obj.inserted_id)), 201


@app.route("/gettoken", methods=["POST"])
def gettoken():
    username = request.json["username"]
    password = request.json["password"]
    role = request.json["role"]

    test = user.find_one({"username": username, "password": password, "role": role})
    if test:
        access_token = create_access_token(identity=(username + " " + role))
        return jsonify(message="Token returned successfully", access_token=access_token), 201
    else:
        return jsonify(message="Bad credentials. User not found"), 401


@app.route("/testdata", methods=["DELETE"])
def testusers():
    splitter_string = '//'
    message_returned = ''

    myquery = {"username": {"$regex": "^ROBOT_TESTING.*"}}
    result = user.delete_many(myquery)
    if result.deleted_count == 0:
        message_returned += "No test users present"
    else:
        message_returned += "Deleted " + str(result.deleted_count) + " Test Users"
    message_returned += splitter_string

    myquery = {"description": {"$regex": "^ROBOT_TESTING.*"}}
    result = serviceapidescriptions.delete_many(myquery)
    if result.deleted_count == 0:
        message_returned += "No test services present"
    else:
        message_returned += "Deleted " + str(result.deleted_count) + " Test Services"
    message_returned += splitter_string

    myquery = {"api_invoker_information": {"$regex": "^ROBOT_TESTING.*"}}
    result = invokerdetails.delete_many(myquery)
    if result.deleted_count == 0:
        message_returned += "No test Invokers present"
    else:
        message_returned += "Deleted " + str(result.deleted_count) + " Test Invokers"
    message_returned += splitter_string

    myquery = {"notification_destination": {"$regex": "^ROBOT_TESTING.*"}}
    result = eventsdetails.delete_many(myquery)
    if result.deleted_count == 0:
        message_returned += "No event subscription present"
    else:
        message_returned += "Deleted " + str(result.deleted_count) + " Event Subscriptions"
    message_returned += splitter_string

    myquery = {"notification_destination": {"$regex": "^ROBOT_TESTING.*"}}
    result = servicesecurity.delete_many(myquery)
    if result.deleted_count == 0:
        message_returned += "No service security subscription present"
    else:
        message_returned += "Deleted " + str(result.deleted_count) + " service security Subscriptions"
    message_returned += splitter_string

    return jsonify(message=message_returned), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
