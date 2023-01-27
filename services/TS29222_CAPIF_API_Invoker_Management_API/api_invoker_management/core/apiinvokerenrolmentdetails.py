from csv import excel
import sys

import rfc3987
import re
import pymongo
from pymongo import ReturnDocument
import secrets
import requests
from .responses import bad_request_error, not_found_error, forbidden_error, internal_server_error, make_response
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder
from ..db.db import MongoDatabse
from ..models.problem_details import ProblemDetails
from ..util import dict_to_camel_case
from .resources import Resource
from bson import json_util

class InvokerManagementOperations(Resource):

    def __check_api_invoker_id(self, api_invoker_id):

        current_app.logger.debug("Cheking api invoker id")
        mycol = self.db.get_col_by_name(self.db.invoker_enrolment_details)
        my_query = {'api_invoker_id':api_invoker_id}
        old_values = mycol.find_one(my_query)

        if old_values is None:
            current_app.logger.error("Not found api invoker id")
            return not_found_error(detail="Please provide an existing Netapp ID", cause= "Not exist NetappID" )

        return old_values

    def __sign_cert(self, publick_key, invoker_information):
        url = "http://easy-rsa:8080/sign-csr"

        payload = dict()
        payload['csr'] = publick_key
        payload['mode'] = 'client'
        payload['filename'] = invoker_information

        headers = {

            'Content-Type': 'application/json'

        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        response_payload = json.loads(response.text)

        return response_payload


    def add_apiinvokerenrolmentdetail(self, apiinvokerenrolmentdetail):

        mycol = self.db.get_col_by_name(self.db.invoker_enrolment_details)

        try:

            current_app.logger.debug("Creating invoker resource")
            res = mycol.find_one({'onboarding_information.api_invoker_public_key': apiinvokerenrolmentdetail.onboarding_information.api_invoker_public_key})

            if res is not None:
                current_app.logger.error("Generating forbbiden error, invoker registered")
                return forbidden_error(detail= "Invoker already registered", cause = "Identical invoker public key")

            if rfc3987.match(apiinvokerenrolmentdetail.notification_destination, rule="URI") is None:
                current_app.logger.error("Bad url format")
                return bad_request_error(detail="Bad Param", cause = "Detected Bad formar of param", invalid_params=[{"param": "notificationDestination", "reason": "Not valid URL format"}])

            current_app.logger.debug("Signing Certificate")

            cert = self.__sign_cert(apiinvokerenrolmentdetail.onboarding_information.api_invoker_public_key, apiinvokerenrolmentdetail.api_invoker_information)

            api_invoker_id = secrets.token_hex(15)
            apiinvokerenrolmentdetail.api_invoker_id = api_invoker_id
            apiinvokerenrolmentdetail.onboarding_information.api_invoker_certificate = cert['certificate']
            mycol.insert_one(apiinvokerenrolmentdetail.to_dict())

            current_app.logger.debug("Invoker inserted in database")
            current_app.logger.debug("Netapp onboarded sucessfuly")

            res = make_response(object=apiinvokerenrolmentdetail, status=201)
            res.headers['Location'] = "/api-invoker-management/v1/onboardedInvokers/" + str(api_invoker_id)
            return res

        except Exception as e:
            exception = "An exception occurred in create invoker"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))

    def update_apiinvokerenrolmentdetail(self, onboard_id, apiinvokerenrolmentdetail):

        mycol = self.db.get_col_by_name(self.db.invoker_enrolment_details)

        try:
            current_app.logger.debug("Updating invoker resource")
            result = self.__check_api_invoker_id(onboard_id)

            if isinstance(result, Response):
                return result

            if apiinvokerenrolmentdetail.onboarding_information.api_invoker_public_key != result["onboarding_information"]["api_invoker_public_key"]:
                cert = self.__sign_cert(apiinvokerenrolmentdetail.onboarding_information.api_invoker_public_key, apiinvokerenrolmentdetail.api_invoker_information)
                apiinvokerenrolmentdetail.onboarding_information.api_invoker_certificate = cert['certificate']

            apiinvokerenrolmentdetail_update = apiinvokerenrolmentdetail.to_dict()
            apiinvokerenrolmentdetail_update = {
                key: value for key, value in apiinvokerenrolmentdetail_update.items() if value is not None
            }

            result = mycol.find_one_and_update(result, {"$set":apiinvokerenrolmentdetail_update}, projection={'_id': 0},return_document=ReturnDocument.AFTER ,upsert=False)

            result = {
                key: value for key, value in result.items() if value is not None
            }

            current_app.logger.debug("Invoker Resource inserted in database")
            res = make_response(object=dict_to_camel_case(result), status=200)
            return res

        except Exception as e:
            exception = "An exception occurred in update invoker"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))

    def remove_apiinvokerenrolmentdetail(self, onboard_id):

        mycol = self.db.get_col_by_name(self.db.invoker_enrolment_details)

        try:
            current_app.logger.debug("Removing invoker resource")
            result = self.__check_api_invoker_id(onboard_id)

            if isinstance(result, Response):
                return result

            mycol.delete_one({'api_invoker_id':onboard_id})

            current_app.logger.debug("Invoker resource removed from database")
            current_app.logger.debug("Netapp offboarded sucessfuly")
            out =  "The Netapp matching onboardingId  " + onboard_id + " was offboarded."
            return make_response(out, status=204)

        except Exception as e:
            exception = "An exception occurred in remove invoker"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))


