#!/usr/bin/env python3

from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
from ..core.register_operations import RegisterOperations
import secrets


register_routes = Blueprint("register_routes", __name__)
register_operation = RegisterOperations()

@register_routes.route("/register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
    description = request.json["description"]
    role = request.json["role"]
    cn = request.json["cn"]
    if role != "invoker" and role != "provider":
        return jsonify(message="Role must be invoker or provider"), 400

    if role == "invoker":
        return register_operation.register_invoker(username, password, description, cn, role)

    elif role == "provider":
        return register_operation.register_provider(username, password, description, cn, role)

@register_routes.route("/getauth", methods=["POST"])
def getauth():
    username = request.json["username"]
    password = request.json["password"]

    return register_operation.get_auth(username, password)

#Pending to remove
@register_routes.route("/testdata", methods=["DELETE"])
def testusers():
    uri = "mongodb://" + "root" + ":" + "example" + "@" + "mongo" + ":" + str(27017)

    myclient = MongoClient(uri)
    mydb = myclient["capif"]
    user = mydb["user"]
    invokerdetails = mydb['invokerdetails']
    serviceapidescriptions = mydb['serviceapidescriptions']
    eventsdetails = mydb['eventsdetails']
    servicesecurity = mydb['servicesecurity']
    providerenrolmentdetails = mydb['providerenrolmentdetails']

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

    myquery = {"api_prov_dom_info": {"$regex": "^ROBOT_TESTING.*"}}
    result = providerenrolmentdetails.delete_many(myquery)
    if result.deleted_count == 0:
        message_returned += "No Provider Enrolment Details present"
    else:
        message_returned += "Deleted " + str(result.deleted_count) + " provider enrolment details"
    message_returned += splitter_string

    return jsonify(message=message_returned), 200

