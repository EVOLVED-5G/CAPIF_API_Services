#!/usr/bin/env python3

import connexion
import sys

from capif_events import encoder


from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
from flask_mqtt import Mqtt
from .db.config import Config
from .core.notifications import Notifications


app = connexion.App(__name__, specification_dir='./openapi/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'CAPIF_Events_API'},
            pythonic_params=True)



config = Config()
config.chargeMQTTConfig(app)

notifications = Notifications()
jwt = JWTManager(app.app)
mqtt = Mqtt(app.app)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
       mqtt.subscribe('/events')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    notifications.send_notifications(data["payload"])

if __name__ == '__main__':
     app.run(debug=True, port=8080)
