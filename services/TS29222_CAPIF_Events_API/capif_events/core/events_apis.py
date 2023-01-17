import sys

import rfc3987
import pymongo
import secrets
import re
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from .resources import Resource
from bson import json_util
from .responses import internal_server_error, not_found_error, make_response, bad_request_error
from ..db.db import MongoDatabse
from ..util import dict_to_camel_case

class EventSubscriptionsOperations(Resource):

    def __check_subscriber_id(self, subscriber_id):
        mycol_invoker= self.db.get_col_by_name(self.db.invoker_collection)
        mycol_provider= self.db.get_col_by_name(self.db.provider_collection)

        current_app.logger.debug("Cheking subscriber id")

        invoker_query = {"api_invoker_id":subscriber_id}

        invoker = mycol_invoker.find_one(invoker_query)

        provider_query = {"api_prov_funcs.api_prov_func_id":subscriber_id}

        provider = mycol_provider.find_one(provider_query)

        if invoker is None and provider is None:
            current_app.logger.error("Not found invoker or provider with this subscriber id")
            return not_found_error(detail="Invoker or APF or AEF or AMF Not found", cause="Subscriber Not Found")

        return None

    def create_event(self, subscriber_id, event_subscription):

        try:
            mycol = self.db.get_col_by_name(self.db.event_collection)

            current_app.logger.debug("Creating event")

            if rfc3987.match(event_subscription.notification_destination, rule="URI") is None:
                current_app.logger.error("Bad url format")
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

            current_app.logger.debug("Event Subscription inserted in database")

            res = make_response(object=event_subscription, status=201)
            res.headers['Location'] = "http://localhost:8080/capif-events/v1/" + \
                str(subscriber_id) + "/subscriptions/" + str(subscription_id)

            return res

        except Exception as e:
            exception = "An exception occurred in create event"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))

    def delete_event(self, subscriber_id, subscription_id):

        try:
            mycol = self.db.get_col_by_name(self.db.event_collection)

            current_app.logger.debug("Removing event subscription")

            result = self.__check_subscriber_id(subscriber_id)


            if  isinstance(result, Response):
                return result

            my_query = {'subscriber_id': subscriber_id,
                    'subscription_id': subscription_id}
            eventdescription = mycol.find_one(my_query)

            if eventdescription is None:
                current_app.logger.error("Event subscription not found")
                return not_found_error(detail="Event subscription not exist", cause="Event API subscription id not found")

            mycol.delete_one(my_query)
            current_app.logger.debug("Event subscription removed from database")

            out =  "The event matching subscriptionId  " + subscription_id + " was deleted."
            return make_response(out, status=204)

        except Exception as e:
            exception= "An exception occurred in delete event"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))


