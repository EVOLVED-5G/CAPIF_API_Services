#!/usr/bin/env python3

import connexion

from service_apis import encoder

import pymongo
import logging
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
from logging.handlers import RotatingFileHandler


def configure_logging(app):
    del app.logger.handlers[:]
    loggers = [app.logger, ]
    handlers = []
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(verbose_formatter())
    file_handler = RotatingFileHandler(filename="discover_logs.log", maxBytes=1024 * 1024 * 100, backupCount=20)
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

app = connexion.App(__name__, specification_dir='./openapi/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'CAPIF_Discover_Service_API'},
            pythonic_params=True)

app.app.config["JWT_SECRET_KEY"] = "this-is-secret-key"
configure_logging(app.app)

jwt = JWTManager(app.app)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
