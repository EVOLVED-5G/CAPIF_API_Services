#!/usr/bin/env python3

import connexion

from capif_events import encoder


from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient


app = connexion.App(__name__, specification_dir='./openapi/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'CAPIF_Events_API'},
            pythonic_params=True)



app.app.config['MONGODB_SETTINGS'] = {
    'user': 'root',
    'password': 'example',
    'db': 'capif',
    'col': 'eventsdetails',
    'jwt': 'user',
    'host': 'mongo',
    'port': 27017,
}


app.app.config["JWT_SECRET_KEY"] = "this-is-secret-key"

jwt = JWTManager(app.app)


if __name__ == '__main__':
     app.run(debug=True, port=8080)
