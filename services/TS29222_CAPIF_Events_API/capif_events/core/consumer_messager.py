# subscriber.py
import redis
import time
import sys
import json
import asyncio
from threading import Thread
from .notifications import Notifications
from .internal_event_ops import InternalEventOperations
from flask import current_app

class Subscriber():

    def __init__(self):
        self.r = redis.Redis(host='redis', port=6379, db=0)
        self.notification = Notifications()
        self.event_ops = InternalEventOperations()
        self.p = self.r.pubsub()
        self.p.subscribe("events", "internal-messages")

    def listen(self):
        for raw_message in self.p.listen():
            if raw_message["type"] == "message" and raw_message["channel"].decode('utf-8') == "events":
                current_app.logger.info("Event received")
                self.notification.send_notifications(raw_message["data"].decode('utf-8'))

            elif raw_message["type"] == "message" and raw_message["channel"].decode('utf-8') == "internal-messages":
                message, *invoker_id = raw_message["data"].decode('utf-8').split(":")
                if message == "invoker-removed":
                    current_app.logger.debug("Recevived message, invoker remove, removing event subscriptions")
                    self.event_ops.delete_all_events(invoker_id[0])



