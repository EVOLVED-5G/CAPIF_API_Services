#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient


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

username = app.config['MONGODB_SETTINGS']['user']
password = app.config['MONGODB_SETTINGS']['password']
db = app.config['MONGODB_SETTINGS']['db']
col = app.config['MONGODB_SETTINGS']['jwt']
host = app.config['MONGODB_SETTINGS']['host']
port = app.config['MONGODB_SETTINGS']['port']

uri = "mongodb://" + username + ":" + password + "@" + host + ":" + str(port)

myclient = MongoClient(uri)
mydb = myclient[db]
user = mydb[col]


@app.route("/register", methods=["POST"])
def register():
    email = request.json["email"]
    test = user.find_one({"email": email})
    if test:
        return jsonify(message="User Already Exist"), 409
    else:
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        password = request.json["password"]
        user_info = dict(first_name=first_name, last_name=last_name, email=email, password=password)
        user.insert_one(user_info)
        return jsonify(message="User added sucessfully"), 201


@app.route("/gettoken", methods=["POST"])
def gettoken():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.json["email"]
        password = request.json["password"]

    test = user.find_one({"email": email, "password": password})
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Bad Email or Password"), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
