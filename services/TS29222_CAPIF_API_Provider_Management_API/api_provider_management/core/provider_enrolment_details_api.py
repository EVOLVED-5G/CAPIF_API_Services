import sys

import pymongo
import secrets
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from ..core.sign_certificate import sign_certificate
from .responses import internal_server_error, not_found_error, forbidden_error, make_response
from bson import json_util
from ..db.db import MongoDatabse
import sys

class ProviderManagementOperations:

    def __init__(self):
        self.db = MongoDatabse()

    def __check_api_provider_domain(self, api_prov_dom_id):
        mycol = self.db.get_col_by_name(self.db.provider_enrolment_details)

        current_app.logger.debug("Checking api provider domain id")
        search_filter = {'api_prov_dom_id': api_prov_dom_id}
        provider_enrolment_details = mycol.find_one(search_filter)

        if provider_enrolment_details is None:
            current_app.logger.error("Not found api provider domain")
            return not_found_error(detail="Not Exist Provider Enrolment Details", cause="Not found registrations to send this api provider details")

        return provider_enrolment_details

    def register_api_provider_enrolment_details(self, api_provider_enrolment_details):
        try:
            mycol = self.db.get_col_by_name(self.db.provider_enrolment_details)

            current_app.logger.debug("Creating api provider domain")
            search_filter = {'reg_sec': api_provider_enrolment_details.reg_sec}
            my_provider_enrolment_details = mycol.find_one(search_filter)

            if my_provider_enrolment_details is not None:
                current_app.logger.error("Found provider registered with same id")
                return forbidden_error(detail="Provider already registered", cause="Identical provider reg sec")

            api_provider_enrolment_details.api_prov_dom_id = secrets.token_hex(15)

            current_app.logger.debug("Geretaing certs to api prov funcs")
            for api_provider_func in api_provider_enrolment_details.api_prov_funcs:
                api_provider_func.api_prov_func_id = secrets.token_hex(15)
                certificate = sign_certificate(api_provider_func.reg_info.api_prov_pub_key, api_provider_func.api_prov_func_info)
                api_provider_func.reg_info.api_prov_cert = certificate


            mycol.insert_one(api_provider_enrolment_details.to_dict())

            current_app.logger.debug("Provider inserted in database")

            res = make_response(object=api_provider_enrolment_details, status=201)
            res.headers['Location'] = "/api-provider-management/v1/registrations/" + str(api_provider_enrolment_details.api_prov_dom_id)
            return res

        except Exception as e:
            exception = "An exception occurred in register provider"
            current_app.logger.error(exception + "::" + e)
            return internal_server_error(cause=exception, detail=e)

    def delete_api_provider_enrolment_details(self, api_prov_dom_id):
        try:
            mycol = self.db.get_col_by_name(self.db.provider_enrolment_details)

            current_app.logger.debug("Deleting provider domain")
            result = self.__check_api_provider_domain(api_prov_dom_id)

            if isinstance(result, Response):
                return result

            mycol.delete_one({'api_prov_dom_id': api_prov_dom_id})
            out =  "The provider matching apiProvDomainId  " + api_prov_dom_id + " was offboarded."
            current_app.logger.debug("Removed provider domain from database")
            return make_response(object=out, status=204)

        except Exception as e:
            exception = "An exception occurred in delete provider"
            current_app.logger.error(exception + "::" + e)
            return internal_server_error(detail=exception, cause=e)

    def update_api_provider_enrolment_details(self, api_prov_dom_id, api_provider_enrolment_details):
        try:
            mycol = self.db.get_col_by_name(self.db.provider_enrolment_details)

            current_app.logger.debug("Updating api provider domain")
            result = self.__check_api_provider_domain(api_prov_dom_id)

            if isinstance(result, Response):
                return result

            api_provider_enrolment_details = api_provider_enrolment_details.to_dict()
            api_provider_enrolment_details = {
                key: value for key, value in api_provider_enrolment_details.items() if value is not None
            }

            mycol.update_one(result, {"$set":api_provider_enrolment_details}, upsert=False)
            current_app.logger.debug("Provider domain updated in database")
            return make_response(object=api_provider_enrolment_details, status=200)

        except Exception as e:
            exception = "An exception occurred in update provider"
            current_app.logger.error(exception + "::" + e)
            return internal_server_error(detail=exception, cause=e)

    def patch_api_provider_enrolment_details(self, api_prov_dom_id, api_provider_enrolment_details_patch):
        try:
            mycol = self.db.get_col_by_name(self.db.provider_enrolment_details)

            current_app.logger.debug("Updating api provider domain")
            result = self.__check_api_provider_domain(api_prov_dom_id)

            if isinstance(result, Response):
                return result

            api_provider_enrolment_details_patch = api_provider_enrolment_details_patch.to_dict()
            api_provider_enrolment_details_patch = {
                key: value for key, value in api_provider_enrolment_details_patch.items() if value is not None
            }

            mycol.update_one(result, {"$set":api_provider_enrolment_details_patch})

            current_app.logger.debug("Provider domain updated in database")

            return make_response(object=api_provider_enrolment_details_patch, status=200)

        except Exception as e:
            exception = "An exception occurred in patch provider"
            current_app.logger.error(exception + "::" + e)
            return internal_server_error(detail=exception, cause=e)