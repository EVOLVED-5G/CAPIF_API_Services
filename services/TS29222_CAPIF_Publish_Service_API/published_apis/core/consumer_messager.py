# subscriber.py
import redis
import time
import sys
import json
import asyncio
from threading import Thread
from .internal_service_ops import InternalServiceOps
from flask import current_app

class Subscriber():

    def __init__(self):
        self.r = redis.Redis(host='redis', port=6379, db=0)
        self.security_ops = InternalServiceOps()
        self.p = self.r.pubsub()
        self.p.subscribe("internal-messages")

    def listen(self):
        current_app.logger.info("Listening publish messages")
        for raw_message in self.p.listen():
            current_app.logger.debug(f"Received message")
            if raw_message["type"] == "message" and raw_message["channel"].decode('utf-8') == "internal-messages":
                message, *ids = raw_message["data"].decode('utf-8').split(":")
                if message == "provider-removed" and len(ids)==2:
                    self.security_ops.delete_intern_service(ids[1])




