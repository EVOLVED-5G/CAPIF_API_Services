import sys

import pymongo
import secrets
import re
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from bson import json_util
from .responses import internal_server_error, not_found_error, make_response, bad_request_error
from ..db.db import MongoDatabse
from ..util import dict_to_camel_case

class EventSubscriptionsOperations:

    def __init__(self):
        self.db = MongoDatabse()

    def __check_subscriber_id(self, subscriber_id):
        mycol_invoker= self.db.get_col_by_name(self.db.invoker_collection)
        mycol_provider= self.db.get_col_by_name(self.db.provider_collection)

        invoker_query = {"api_invoker_id":subscriber_id}

        invoker = mycol_invoker.find_one(invoker_query)

        provider_query = {"api_prov_funcs.api_prov_func_id":subscriber_id}

        provider = mycol_provider.find_one(provider_query)

        if invoker is None and provider is None:
            return not_found_error(detail="Not found Subscriber", cause="Not found Invoker or APF or AEF or AMF")

        return None

    def create_event(self, subscriber_id, event_subscription):

        try:
            mycol = self.db.get_col_by_name(self.db.event_collection)

            if not re.match("^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$", event_subscription.notification_destination):

                return bad_request_error(detail="Bad Param", cause = "Detected Bad formar of param", invalid_params=[{"param": "notificationDestination", "reason": "Not valid URL format"}])

            ## Verify that this subscriberID exist in publishers or invokers

            result = self.__check_subscriber_id(subscriber_id)


            if  isinstance(result, Response):

                return result

            # Generate subscriptionID
            subscription_id = secrets.token_hex(15)
            evnt = dict()
            evnt["subscriber_id"] = subscriber_id
            evnt["subscription_id"] = subscription_id
            evnt.update(event_subscription.to_dict())
            mycol.insert_one(evnt)


            res = make_response(object=event_subscription, status=201)
            res.headers['Location'] = "http://localhost:8080/capif-events/v1/" + \
                str(subscriber_id) + "/subscriptions/" + str(subscription_id)
            return res

        except Exception as e:
            exception = "An exception occurred in create event"
            return internal_server_error(detail=exception, cause=e)

    def delete_event(self, subscriber_id, subscription_id):

        try:
            mycol = self.db.get_col_by_name(self.db.event_collection)
            result = self.__check_subscriber_id(subscriber_id)


            if  isinstance(result, Response):
                return result

            myQuery = {'subscriber_id': subscriber_id,
                    'subscription_id': subscription_id}
            eventdescription = mycol.find_one(myQuery)

            if eventdescription is None:
                return not_found_error(detail="Service API not existing", cause="Event API subscription id not found")

            mycol.delete_one(myQuery)
            out =  "The event matching subscriptionId  " + subscription_id + " was deleted."
            return make_response(out, status=204)

        except Exception as e:
            exception= "An exception occurred in delete event"
            return internal_server_error(detail=exception, cause=e)
