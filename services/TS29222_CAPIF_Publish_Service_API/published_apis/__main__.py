#!/usr/bin/env python3

import connexion

from published_apis import encoder

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
from flask_mqtt import Mqtt


app = connexion.App(__name__, specification_dir='./openapi/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'CAPIF_Publish_Service_API'},
            pythonic_params=True)

app.app.config["JWT_SECRET_KEY"] = "this-is-secret-key"

app.app.config['MQTT_BROKER_URL'] = 'mosquitto'  # use the free broker from HIVEMQ
app.app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

jwt = JWTManager(app.app)
mqtt = Mqtt(app.app)
app.app.config["INSTANCE_MQTT"] = mqtt



if __name__ == '__main__':
    app.run(debug=True, port=8080)
