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
        current_app.logger.info("Listening security context messages")
        for raw_message in self.p.listen():
            if raw_message["type"] == "message" and raw_message["channel"].decode('utf-8') == "internal-messages":
                message, *ids = raw_message["data"].decode('utf-8').split(":")
                if message == "invoker-removed":
                    self.security_ops.delete_intern_servicesecurity(ids[0])
                if message == "provider-removed" or message == "service-removed":
                    self.security_ops.update_intern_servicesecurity(ids[0])
                




