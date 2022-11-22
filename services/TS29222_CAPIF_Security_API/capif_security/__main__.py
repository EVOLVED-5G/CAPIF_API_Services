#!/usr/bin/env python3

import connexion
import logging
from capif_security import encoder
from flask_jwt_extended import JWTManager
from .config import Config
from .core.consumer_messager import Subscriber
from threading import Thread
from flask_executor import Executor
from flask_apscheduler import APScheduler
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

    jwt = JWTManager(app.app)
    subscriber = Subscriber()
    scheduler = APScheduler()
    scheduler.init_app(app.app)
    configure_logging(app.app)

    # @scheduler.task('interval', id='do_job_1', seconds=10, misfire_grace_time=900)
    # def job1():
    #     with scheduler.app.app_context():
    #         subscriber.get_message()

    # scheduler.start()

    executor = Executor(app.app)

    @app.app.before_first_request
    def up_listener():
        executor.submit(subscriber.listen)


    app.run(port=8080, debug=True)

if __name__ == '__main__':
    main()

