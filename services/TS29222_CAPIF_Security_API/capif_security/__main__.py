#!/usr/bin/env python3

import connexion
import logging
from capif_security import encoder
from flask_jwt_extended import JWTManager
from .config import Config
from flask_mqtt import Mqtt
import sys


def configure_logging(app):
    del app.logger.handlers[:]
    loggers = [app.logger, ]
    handlers = []
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(verbose_formatter())
    handlers.append(console_handler)

    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)

def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

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

    config = Config()
    config.chargeMQTTConfig(app)

    jwt = JWTManager(app.app)
    mqtt = Mqtt(app.app)
    app.app.config["INSTANCE_MQTT"] = mqtt

    configure_logging(app.app)

    app.run(port=8080, debug=True)

if __name__ == '__main__':
    main()

