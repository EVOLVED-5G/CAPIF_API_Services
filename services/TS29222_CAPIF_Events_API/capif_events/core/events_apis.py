import sys

import pymongo
import secrets
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from bson import json_util
from ..lib.db import MongoDatabse

class EventSubscriptionsOperations:

    def __init__(self):
        self.db = MongoDatabse()

    def create_event(self, subscriber_id, event_subscription):

        try:
            mycol = self.db.get_col_by_name(self.db.event_collection)
            mycol_user= self.db.get_col_by_name(self.db.user_collection)


            ## Verify that this subscriberID exist in publishers or invokers

            query= {'_id':subscriber_id}
            check = mycol_user.find_one(query)


            if  check is None:

                prob = ProblemDetails(title="Not Found", status=403, detail="Event API not existing",
                                    cause="Event Subscriptions are not stored in CAPIF Database")
                return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')

            # Generate subscriptionID
            subscription_id = secrets.token_hex(15)
            evnt = dict()
            evnt["subscriber_id"] = subscriber_id
            evnt["subscription_id"] = subscription_id
            evnt.update(event_subscription.to_dict())
            mycol.insert_one(evnt)

            res = Response(json.dumps(event_subscription, cls=JSONEncoder),
                        status=201, mimetype='application/json')
            res.headers['Location'] = "http://localhost:8080/capif-events/v1/" + \
                str(subscriber_id) + "/subscriptions/" + str(subscription_id)
            return res

        except Exception as e:
            print("An exception occurred ::", e)
            return False

    def delete_event(self, subscriber_id, subscription_id):

        try:
            mycol = self.db.get_col_by_name(self.db.event_collection)
            mycol_user=self.db.get_col_by_name(self.db.user_collection)

            query= {'_id':subscriber_id}
            check = mycol_user.find_one(query)


            if  check is None:
                prob = ProblemDetails(title="Not Found", status=403, detail="Event API not existing",
                                    cause="Event Subscriptions are not stored in CAPIF Database")
                return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')

            myQuery = {'subscriber_id': subscriber_id,
                    'subscription_id': subscription_id}
            eventdescription = mycol.find_one(myQuery)

            if eventdescription is None:
                prob = ProblemDetails(title="Not Found", status=404, detail="Service API not existing",
                                    cause="Event API subscription id not found")
                return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype='application/json')
            else:
                mycol.delete_one(myQuery)
                return Response(json.dumps(eventdescription, default=str, cls=JSONEncoder), status=204, mimetype='application/json')

        except Exception as e:
            print("An exception occurred ::", e)
            return False

    def get_event_subscriptions(self, event):
        try:
            mycol = self.db.get_col_by_name(self.db.event_collection)

            query= {'events':event}
            subscriptions = mycol.find(query)


            if  subscriptions is None:
                prob = ProblemDetails(title="Not Found", status=404, detail="Not Exist subscriptions",
                                    cause="Not found subscriptions to send this event")
                return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')

            else:
                json_docs=[]
                for subscription in subscriptions:
                    json_docs.append(subscription)

                return json_docs

        except Exception as e:
            print("An exception occurred ::", e)
            return False
