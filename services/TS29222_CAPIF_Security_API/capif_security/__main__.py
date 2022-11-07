#!/usr/bin/env python3

import connexion

from capif_security import encoder
from flask_jwt_extended import JWTManager
from flask_mqtt import Mqtt
import sys


def main():

    with open("/usr/src/app/capif_security/server.key", "rb") as key_file:
            key_data = key_file.read()

    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder

    jwt = JWTManager(app.app)
    app.app.config['JWT_ALGORITHM'] = 'RS256'
    app.app.config['JWT_PRIVATE_KEY'] = key_data
    app.add_api('openapi.yaml',
                arguments={'title': 'CAPIF_Security_API'},
                pythonic_params=True)

    app.app.config['MQTT_BROKER_URL'] = 'mosquitto'  # use the free broker from HIVEMQ
    app.app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    jwt = JWTManager(app.app)
    mqtt = Mqtt(app.app)
    app.app.config["INSTANCE_MQTT"] = mqtt

    app.run(port=8080, debug=True)

if __name__ == '__main__':
    main()

