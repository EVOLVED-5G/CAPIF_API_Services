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

app.config["JWT_SECRET_KEY"] = "this-is-secret-key"

jwt = JWTManager(app)

user = app.config['MONGODB_SETTINGS']['user']
passwd = app.config['MONGODB_SETTINGS']['password']
db = app.config['MONGODB_SETTINGS']['db']
col = app.config['MONGODB_SETTINGS']['jwt']
host = app.config['MONGODB_SETTINGS']['host']
port = app.config['MONGODB_SETTINGS']['port']

uri = "mongodb://" + user + ":" + passwd + "@" + host + ":" + str(port)

myclient = MongoClient(uri)
mydb = myclient[db]
user = mydb[col]


@app.route("/register", methods=["POST"])
def register():
    username = request.json["username"]
    test = user.find_one({"username": username})
    if test:
        return jsonify(message="User Already Exist"), 409
    elif request.json["role"] != "invoker" and request.json["role"] != "apf":
        return jsonify(message="Role must be invoker or apf"), 409
    else:
        username = request.json["username"]
        password = request.json["password"]
        role = request.json["role"]
        hostip = request.json["hostip"]
        email = request.json["email"]
        user_info = dict(_id=secrets.token_hex(7), username=username, password=password, role=role, hostip=hostip, email=email)
        obj = user.insert_one(user_info)
        return jsonify(message="User added sucessfully", id=obj.inserted_id), 201


@app.route("/gettoken", methods=["POST"])
def gettoken():
    username = request.json["username"]
    password = request.json["password"]

    test = user.find_one({"username": username, "password": password})
    if test:
        access_token = create_access_token(identity=username)
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Bad username or password"), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
