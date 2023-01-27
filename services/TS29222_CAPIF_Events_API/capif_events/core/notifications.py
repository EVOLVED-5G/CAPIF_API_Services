#import concurrent
import requests
from .internal_event_ops import InternalEventOperations
from ..models.event_notification import EventNotification
from ..encoder import JSONEncoder
import sys
import json
from flask import current_app

class Notifications():

    def __init__(self):
        self.events_ops = InternalEventOperations()

    def send_notifications(self, event):
        current_app.logger.info("Received event, sending notifications")
        subscriptions = self.events_ops.get_event_subscriptions(event)

        for sub in subscriptions:
            url = sub["notification_destination"]
            data = EventNotification(sub["subscription_id"], events=event)
            self.request_post(url, data)

    def request_post(self, url, data):
        headers = {'content-type': 'application/json'}
        return requests.post(url, json={'text': str(data.to_str())}, headers=headers)

