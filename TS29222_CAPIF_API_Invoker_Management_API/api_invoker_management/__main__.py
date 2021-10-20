#!/usr/bin/env python3

import connexion

from api_invoker_management import encoder

import pymongo
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient


app = connexion.App(__name__, specification_dir='./openapi/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'CAPIF_API_Invoker_Management_API'},
            pythonic_params=True)
app.app.config['MONGODB_SETTINGS'] = {
    'user': 'root',
    'password': 'example',
    'db': 'capif',
    'col': 'invokerdetails',
    'jwt': 'user',
    'host': 'mongo',
    'port': 27017,
}

app.app.config["JWT_SECRET_KEY"] = "this-is-secret-key"

jwt = JWTManager(app.app)

username = app.app.config['MONGODB_SETTINGS']['user']
password = app.app.config['MONGODB_SETTINGS']['password']
db = app.app.config['MONGODB_SETTINGS']['db']
col = app.app.config['MONGODB_SETTINGS']['jwt']
host = app.app.config['MONGODB_SETTINGS']['host']
port = app.app.config['MONGODB_SETTINGS']['port']

uri = "mongodb://" + username + ":" + password + "@" + host + ":" + str(port)

myclient = pymongo.MongoClient(uri)
mydb = myclient[db]
user = mydb[col]


@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    test = user.find_one({"email": email})
    if test:
        return jsonify(message="User Already Exist"), 409
    else:
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        user_info = dict(first_name=first_name, last_name=last_name, email=email, password=password)
        user.insert_one(user_info)
        return jsonify(message="User added sucessfully"), 201


@app.route("/gettoken", methods=["POST"])
def gettoken():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]

    test = user.find_one({"email": email, "password": password})
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Bad Email or Password"), 401


if __name__ == '__main__':
    app.run(debug=True, port=8080)
