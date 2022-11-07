import requests
from ..encoder import JSONEncoder
import sys
import json

class Notifications():

    def send_notification(self, url, data):

        self.request_post(url, data)

    def request_post(self, url, data):
        headers = {'content-type': 'application/json'}
        return requests.post(url, json={'text': str(data.to_str())}, headers=headers)