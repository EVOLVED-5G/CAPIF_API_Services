#import concurrent
import requests
from .events_apis import EventSubscriptionsOperations
from ..models.event_notification import EventNotification
from ..encoder import JSONEncoder
import sys
import json

class Notifications():

    def __init__(self):
        self.events_ops = EventSubscriptionsOperations()

    def send_notifications(self, event):
        subscriptions = self.events_ops.get_event_subscriptions(event)

        for sub in subscriptions:
            url = sub["notification_destination"]
            data = EventNotification(sub["subscription_id"], events=event)
            self.request_post(url, data)
            #res = executor.map(self.request_post, url, data)
        #concurrent.futures.wait(res)

    def request_post(self, url, data):
        headers = {'content-type': 'application/json'}
        return requests.post(url, json={'text': str(data.to_str())}, headers=headers)

