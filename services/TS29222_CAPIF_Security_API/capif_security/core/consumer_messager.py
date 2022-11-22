# subscriber.py
import redis
import time
import sys
import json
import asyncio
from threading import Thread
from .internal_security_ops import InternalSecurityOps
from flask import current_app

class Subscriber():

    def __init__(self):
        self.r = redis.Redis(host='redis', port=6379, db=0)
        self.security_ops = InternalSecurityOps()
        self.p = self.r.pubsub()
        self.p.subscribe("internal-messages")

    def listen(self):
        for raw_message in self.p.listen():
            if raw_message["type"] == "message" and raw_message["channel"].decode('utf-8') == "internal-messages":
                message, invoker_id = raw_message["data"].decode('utf-8').split(":")
                if message == "invoker-removed":
                    self.security_ops.delete_intern_servicesecurity(invoker_id)

    # def get_message(self):
    #     message = self.p.get_message()
    #     if message != None:
    #         if message["type"] == "message" and message["channel"].decode('utf-8') == "internal-messages":
    #                 message, invoker_id = message["data"].decode('utf-8').split(":")
    #                 if message == "invoker-removed":
    #                     self.security_ops.delete_intern_servicesecurity(invoker_id)



