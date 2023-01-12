#!/usr/bin/env python3

import connexion
import logging

from api_provider_management import encoder
from flask_jwt_extended import JWTManager
from logging.handlers import RotatingFileHandler


def configure_logging(app):
    del app.logger.handlers[:]
    loggers = [app.logger, ]
    handlers = []
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(verbose_formatter())
    file_handler = RotatingFileHandler(filename="provider_logs.log", maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(verbose_formatter())
    handlers.append(console_handler)
    handlers.append(file_handler)

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

    with open("/usr/src/app/api_provider_management/pubkey.pem", "rb") as pub_file:
            pub_data = pub_file.read()

    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'CAPIF_API_Provider_Management_API'},
                pythonic_params=True)

    configure_logging(app.app)
    app.app.config['JWT_ALGORITHM'] = 'RS256'
    app.app.config['JWT_PUBLIC_KEY'] = pub_data

    JWTManager(app.app)


    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
