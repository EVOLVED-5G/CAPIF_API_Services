import redis
import sys

class Publisher():

    def __init__(self):
        self. r = redis.Redis(host='redis', port=6379, db=0)

    def publish_message(self, channel, message):
        self.r.publish(channel, message)