import sys

import pymongo
from pymongo import ReturnDocument
import secrets
from flask import current_app, Flask, Response
import json

from pymongo import response
from ..db.db import MongoDatabse
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from .resources import Resource
from ..util import dict_to_camel_case, clean_empty
from .responses import bad_request_error, internal_server_error, forbidden_error, not_found_error, unauthorized_error, make_response
from bson import json_util


service_api_not_found_message = "Service API not found"

class PublishServiceOperations(Resource):

    def __check_apf(self, apf_id):
        providers_col = self.db.get_col_by_name(self.db.capif_provider_col)

        current_app.logger.debug("Checking apf id")
        provider = providers_col.find_one({"api_prov_funcs.api_prov_func_id": apf_id})

        if provider is None:
            current_app.logger.error("Publisher not exist")
            return unauthorized_error(detail = "Publisher not existing", cause = "Publisher id not found")

        list_apf_ids =  [func["api_prov_func_id"] for func in provider["api_prov_funcs"] if func["api_prov_func_role"] == "APF"]
        if apf_id not in list_apf_ids:
            current_app.logger.debug("This id not belongs to APF")
            return unauthorized_error(detail ="You are not a publisher", cause ="This API is only available for publishers")

        return None


    def get_serviceapis(self, apf_id):

        mycol = self.db.get_col_by_name(self.db.service_api_descriptions)

        try:

            current_app.logger.debug("Geting service apis")
           
            result = self.__check_apf(apf_id)

            if result != None:
                return result

            service = mycol.find({"apf_id": apf_id}, {"apf_id":0, "_id":0})
            if service is None:
                current_app.logger.error("Not found services for this apf id")
                return not_found_error(detail="Not exist published services for this apf_id", cause="Not exist service with this apf_id")

            json_docs = []
            for serviceapi in service:
                my_service_api = dict_to_camel_case(serviceapi)
                my_service_api = clean_empty(my_service_api)
                json_docs.append(my_service_api)

            current_app.logger.debug("Obtained services apis")

            res = make_response(object=json_docs, status=200)
            return res

        except Exception as e:
            exception = "An exception occurred in get services"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))

    def add_serviceapidescription(self, apf_id, serviceapidescription):

        mycol = self.db.get_col_by_name(self.db.service_api_descriptions)

        try:

            current_app.logger.debug("Publishing service")
            result = self.__check_apf(apf_id)

            if result != None:
                return result

            service = mycol.find_one({"api_name": serviceapidescription.api_name})
            if service is not None:
                current_app.logger.error("Service already registered with same api name")
                return forbidden_error(detail="Already registered service with same api name", cause="Found service with same api name")

            api_id = secrets.token_hex(15)
            serviceapidescription.api_id = api_id
            rec = dict()
            rec['apf_id'] = apf_id
            rec.update(serviceapidescription.to_dict())
            mycol.insert_one(rec)

            current_app.logger.debug("Service inserted in database")
            res = make_response(object=serviceapidescription, status=201)
            res.headers['Location'] = "http://localhost:8080/published-apis/v1/" + str(apf_id) + "/service-apis/" + str(api_id)

            return res

        except Exception as e:
            exception = "An exception occurred in add services"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))



    def get_one_serviceapi(self, service_api_id, apf_id):

        mycol = self.db.get_col_by_name(self.db.service_api_descriptions)

        try:
            current_app.logger.debug("Geting service api with id: " + service_api_id)
            result = self.__check_apf(apf_id)

            if result != None:
                return result

            my_query = {'apf_id': apf_id, 'api_id': service_api_id}
            service_api = mycol.find_one(my_query, {"apf_id":0, "_id":0})
            if service_api is None:
                current_app.logger.error(service_api_not_found_message)
                return not_found_error(detail=service_api_not_found_message, cause="No Service with specific credentials exists")


            my_service_api = dict_to_camel_case(service_api)
            my_service_api = clean_empty(my_service_api)

            current_app.logger.debug("Obtained service api")
            res = make_response(object=my_service_api, status=200)
            return res

        except Exception as e:
            exception = "An exception occurred in get one service"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))

    def delete_serviceapidescription(self, service_api_id, apf_id):

        mycol = self.db.get_col_by_name(self.db.service_api_descriptions)

        try:

            current_app.logger.debug("Removing api service with id: " + service_api_id)
            result = self.__check_apf(apf_id)

            if result != None:
                return result

            my_query = {'apf_id': apf_id, 'api_id': service_api_id}
            serviceapidescription = mycol.find_one(my_query)

            if serviceapidescription is None:
                current_app.logger.error(service_api_not_found_message)
                return not_found_error(detail="Service API not existing", cause="Service API id not found")

            mycol.delete_one(my_query)

            current_app.logger.debug("Removed service from database")
            out =  "The service matching api_id " + service_api_id + " was deleted."
            return make_response(out, status=204)

        except Exception as e:
            exception = "An exception occurred in delete service"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))


    def update_serviceapidescription(self, service_api_id, apf_id, service_api_description):

        mycol = self.db.get_col_by_name(self.db.service_api_descriptions)

        try:

            current_app.logger.debug("Updating service api with id: " + service_api_id)

            result = self.__check_apf(apf_id)

            if result != None:
                return result

            my_query = {'apf_id': apf_id, 'api_id': service_api_id}
            serviceapidescription = mycol.find_one(my_query)

            if serviceapidescription is None:
                current_app.logger.error(service_api_not_found_message)
                return not_found_error(detail="Service API not existing", cause="Service API id not found")

            service_api_description = service_api_description.to_dict()
            service_api_description = clean_empty(service_api_description)

            result = mycol.find_one_and_update(serviceapidescription, {"$set":service_api_description}, projection={"apf_id":0, "_id":0},return_document=ReturnDocument.AFTER ,upsert=False)

            result = clean_empty(result)

            current_app.logger.debug("Updated service api")
    
            response = make_response(object=dict_to_camel_case(result), status=200)

            return response

        except Exception as e:
            exception = "An exception occurred in update service"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))

