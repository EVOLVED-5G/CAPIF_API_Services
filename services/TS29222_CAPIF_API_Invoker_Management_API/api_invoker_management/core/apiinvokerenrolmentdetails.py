import sys

import re
import pymongo
import secrets
import requests
from .responses import bad_request_error, not_found_error, forbidden_error, internal_server_error, make_response
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder
from ..db.db import MongoDatabse
from ..models.problem_details import ProblemDetails

class InvokerManagementOperations:

    def __init__(self):
        self.db = MongoDatabse()

    def __check_api_invoker_id(self, api_invoker_id):

        mycol = self.db.get_col_by_name(self.db.invoker_enrolment_details)
        myQuery = {'api_invoker_id':api_invoker_id}
        old_values = mycol.find_one(myQuery)

        if old_values is None:

            return not_found_error(detail="Please provide an existing Netapp ID", cause= "Not exist NetappID" )

        return old_values

    def add_apiinvokerenrolmentdetail(self, apiinvokerenrolmentdetail):

        mycol = self.db.get_col_by_name(self.db.invoker_enrolment_details)

        try:

            res = mycol.find_one({'onboarding_information.api_invoker_public_key': apiinvokerenrolmentdetail.onboarding_information.api_invoker_public_key})

            if res is not None:

                return forbidden_error(detail= "Invoker already registered", cause = "Identical invoker public key")


            if not re.match("^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$", apiinvokerenrolmentdetail.notification_destination):

                return bad_request_error(detail="Bad Param", cause = "Detected Bad formar of param", invalid_params=[{"param": "notificationDestination", "reason": "Not valid URL format"}])

            else:

                url = "http://easy-rsa:8080/sign-csr"

                payload = dict()
                payload['csr'] = apiinvokerenrolmentdetail.onboarding_information.api_invoker_public_key
                payload['mode'] = 'client'
                payload['filename'] = apiinvokerenrolmentdetail.api_invoker_information

                headers = {

                    'Content-Type': 'application/json'

                }

                response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
                response_payload = json.loads(response.text)

                api_invoker_id = secrets.token_hex(15)
                apiinvokerenrolmentdetail.api_invoker_id = api_invoker_id
                apiinvokerenrolmentdetail.onboarding_information.api_invoker_certificate = response_payload['certificate']
                mycol.insert_one(apiinvokerenrolmentdetail.to_dict())

                res = make_response(object= apiinvokerenrolmentdetail, status=201)
                res.headers['Location'] = "/api-invoker-management/v1/onboardedInvokers/" + str(api_invoker_id)
                return res

        except Exception as e:
            exception = "An exception occurred in create invoker"
            return internal_server_error(detail=exception, cause=e)

    def update_apiinvokerenrolmentdetail(self, onboard_id, apiinvokerenrolmentdetail):

        mycol = self.db.get_col_by_name(self.db.invoker_enrolment_details)

        try:
            result = self.__check_api_invoker_id(onboard_id)

            if isinstance(result, Response):
                return result

            apiinvokerenrolmentdetail = apiinvokerenrolmentdetail.to_dict()
            apiinvokerenrolmentdetail = {
                key: value for key, value in apiinvokerenrolmentdetail.items() if value is not None
            }

            mycol.update_one(result, {"$set":apiinvokerenrolmentdetail}, upsert=False)


            res = make_response(object=apiinvokerenrolmentdetail, status=200)
            return res

        except Exception as e:
            exception = "An exception occurred in update invoker"
            return internal_server_error(detail=exception, cause=e)

    def remove_apiinvokerenrolmentdetail(self, onboard_id):

        mycol = self.db.get_col_by_name(self.db.invoker_enrolment_details)

        try:
            result = self.__check_api_invoker_id(onboard_id)

            if isinstance(result, Response):
                return result

            mycol.delete_one({'api_invoker_id':onboard_id})
            out =  "The Netapp matching onboardingId  " + onboard_id + " was offboarded."
            return make_response(out, status=204)

        except Exception as e:
            exception = "An exception occurred in remove invoker"
            return internal_server_error(detail=exception, cause=e)


