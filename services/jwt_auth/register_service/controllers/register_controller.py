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

@register_routes.route("/remove", methods=["DELETE"])
def remove():
    username = request.json["username"]
    password = request.json["password"]

    return register_operation.remove_user(username, password)

#Pending to remove
@register_routes.route("/testdata", methods=["DELETE"])
def testusers():
    return register_operation.delete_tests()
    