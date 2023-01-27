# subscriber.py
import redis
from .invoker_internal_ops import InvokerInternalOperations
from flask import current_app

class Subscriber():

    def __init__(self):
        self.r = redis.Redis(host='redis', port=6379, db=0)
        self.invoker_ops = InvokerInternalOperations()
        self.p = self.r.pubsub()
        self.p.subscribe("internal-messages")

    def listen(self):
        for raw_message in self.p.listen():
            if raw_message["type"] == "message" and raw_message["channel"].decode('utf-8') == "internal-messages":
                message, invoker_id, api_id = raw_message["data"].decode('utf-8').split(":")
                if message == "security-context-created":
                    current_app.logger.debug("Internal message received, updating Api list on invoker")
                    self.invoker_ops.update_services_list(invoker_id, api_id)
                if message == "security-context-removed":
                    current_app.logger.debug("Internal message received, removing service in  Api list of invoker")
                    self.invoker_ops.remove_services_list(invoker_id, api_id)



