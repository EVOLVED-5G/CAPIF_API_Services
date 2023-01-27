import sys

import pymongo
from pymongo import ReturnDocument
import secrets
import re
import rfc3987
from flask import current_app, Flask, Response
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
import json

from ..db.db import MongoDatabse
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from ..models.access_token_rsp import AccessTokenRsp
from ..models.access_token_claims import AccessTokenClaims
from bson import json_util
import requests
from ..models.access_token_err import AccessTokenErr
from ..models.service_security import ServiceSecurity
from ..util import dict_to_camel_case, clean_empty
from .responses import not_found_error, make_response, bad_request_error, internal_server_error, forbidden_error
from .notification import Notifications
from .resources import Resource
import os

security_context_not_found_detail = "Security context not found"
api_invoker_no_context_cause = "API Invoker has no security context"

class SecurityOperations(Resource):

    def __check_invoker(self, api_invoker_id):
        invokers_col = self.db.get_col_by_name(self.db.capif_invokers)

        current_app.logger.debug("Checking api invoker with id: " + api_invoker_id)
        invoker =  invokers_col.find_one({"api_invoker_id": api_invoker_id})
        if invoker is None:
            current_app.logger.error("Invoker not found")
            return not_found_error(detail="Invoker not found", cause="API Invoker not exists or invalid ID")

        return None

    def __check_scope(self, scope, security_context):

        try:

            current_app.logger.debug("Checking scope")
            header = scope[0:4]
            if header != "3gpp":
                current_app.logger.error("Bad format scope")
                token_error = AccessTokenErr(error="invalid_scope", error_description="The first characters must be '3gpp'")
                return make_response(object=token_error, status=400)

            _, body = scope.split("#")

            capif_service_col = self.db.get_col_by_name(self.db.capif_service_col)
            security_info = security_context["security_info"]
            aef_security_context = [info["aef_id"] for info in security_info]

            groups = body.split(";")
            for group in groups:
                aef_id, api_names = group.split(":")
                if aef_id not in aef_security_context:
                    current_app.logger.error("Bad format Scope, not valid aef id ")
                    token_error = AccessTokenErr(error="invalid_scope", error_description="One of aef_id not belongs of your security context")
                    return make_response(object=token_error, status=400)
                api_names = api_names.split(",")
                for api_name in api_names:
                    service = capif_service_col.find_one({"$and": [{"api_name":api_name},{self.filter_aef_id:aef_id}]})
                    if service is None:
                        current_app.logger.error("Bad format Scope, not valid api name")
                        token_error = AccessTokenErr(error="invalid_scope", error_description="One of the api names does not exist or is not associated with the aef id provided")
                        return make_response(object=token_error, status=400)

            return None

        except Exception as e:
            current_app.logger.error("Bad format Scope: " + e)
            token_error = AccessTokenErr(error="invalid_scope", error_description="malformed scope")
            return make_response(object=token_error, status=400)

    def __init__(self):
        Resource.__init__(self)
        self.filter_aef_id = "aef_profiles.aef_id"

    def get_servicesecurity(self, api_invoker_id, authentication_info=True, authorization_info=True):

        mycol = self.db.get_col_by_name(self.db.security_info)

        try:

            current_app.logger.debug("Obtainig security context with id: " + api_invoker_id)
            result = self.__check_invoker(api_invoker_id)
            if result != None:
                return result
            else:
                services_security_object = mycol.find_one({"api_invoker_id": api_invoker_id}, {"_id":0, "api_invoker_id":0})

                if services_security_object is None:
                    current_app.logger.error("Not found security context")
                    return not_found_error(detail= security_context_not_found_detail, cause=api_invoker_no_context_cause)

                if not authentication_info:
                    for security_info_obj in services_security_object['security_info']:
                        del security_info_obj['authentication_info']
                if not authorization_info:
                    for security_info_obj in services_security_object['security_info']:
                        del security_info_obj['authorization_info']

                properyly_json= json.dumps(services_security_object, default=json_util.default)
                my_service_security = dict_to_camel_case(json.loads(properyly_json))
                my_service_security = clean_empty(my_service_security)

                current_app.logger.debug("Obtained security context from database")
        
                res = make_response(object=my_service_security, status=200)

                return res
        except Exception as e:
            exception = "An exception occurred in get security info"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))


    def create_servicesecurity(self, api_invoker_id, service_security):

        mycol = self.db.get_col_by_name(self.db.security_info)

        try:

            current_app.logger.debug("Creating security context")
            result = self.__check_invoker(api_invoker_id)
            if result != None:
                return result

            if rfc3987.match(service_security.notification_destination, rule="URI") is None:
                current_app.logger.error("Bad url format")
                return bad_request_error(detail="Bad Param", cause = "Detected Bad format of param", invalid_params=[{"param": "notificationDestination", "reason": "Not valid URL format"}])

            services_security_object = mycol.find_one({"api_invoker_id": api_invoker_id})

            if services_security_object is not None:

                current_app.logger.error("Already security context defined with same api invoker id")
                return forbidden_error(detail="Security method already defined", cause="Identical AEF Profile IDs")


            for service_instance in service_security.security_info:
                if service_instance.interface_details is not None:
                    security_methods = service_instance.interface_details.security_methods
                    pref_security_methods = service_instance.pref_security_methods
                    valid_security_method = set(security_methods) & set(pref_security_methods)

                else:
                    capif_service_col = self.db.get_col_by_name(self.db.capif_service_col)
                    services_security_object = capif_service_col.find_one({"api_id":service_instance.api_id, self.filter_aef_id: service_instance.aef_id}, {"aef_profiles.security_methods.$":1})

                    if services_security_object is None:
                        current_app.logger.error("Not found service with this aef id: " + service_instance.aef_id)
                        return not_found_error(detail="Service with this aefId not found", cause="Not found Service")

                    pref_security_methods = service_instance.pref_security_methods
                    valid_security_methods = [security_method for array_methods in services_security_object["aef_profiles"] for security_method in array_methods["security_methods"]]
                    valid_security_method = set(valid_security_methods) & set(pref_security_methods)

                if len(list(valid_security_method)) == 0:
                    current_app.logger.error("Not found comptaible security method with pref security method")
                    return bad_request_error(detail="Not found compatible security method with pref security method", cause="Error pref security method", invalid_params=[{"param": "prefSecurityMethods", "reason": "pref security method not compatible with security method available"}])

                service_instance.sel_security_method = list(valid_security_method)[0]

            rec = dict()
            rec['api_invoker_id'] = api_invoker_id
            rec.update(service_security.to_dict())
            mycol.insert_one(rec)

            current_app.logger.debug("Inserted security context in database")

            res = make_response(object=service_security, status=201)
            res.headers['Location'] = "https://{}/capif-security/v1/trustedInvokers/{}".format(os.getenv('CAPIF_HOSTNAME'),str(api_invoker_id))
            return res

        except Exception as e:
            exception = "An exception occurred in create security info"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))


    def delete_servicesecurity(self, api_invoker_id):

        mycol = self.db.get_col_by_name(self.db.security_info)

        try:

            current_app.logger.debug("Removing security context")

            result = self.__check_invoker(api_invoker_id)
            if result != None:
                return result
            else:
                my_query = {'api_invoker_id': api_invoker_id}
                services_security_count = mycol.count_documents(my_query)

                if services_security_count == 0:
                    current_app.logger.error(security_context_not_found_detail)
                    return not_found_error(detail=security_context_not_found_detail, cause=api_invoker_no_context_cause)

                mycol.delete_many(my_query)

                current_app.logger.debug("Removed security context from database")
                out= "The security info of Netapp with Netapp ID " + api_invoker_id + " were deleted.", 204
                return make_response(out, status=204)

        except Exception as e:
            exception = "An exception occurred in create security info"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause = str(e))

    def delete_intern_servicesecurity(self, api_invoker_id):

        mycol = self.db.get_col_by_name(self.db.security_info)
        my_query = {'api_invoker_id': api_invoker_id}
        mycol.delete_many(my_query)

    def return_token(self, security_id, access_token_req):

        mycol = self.db.get_col_by_name(self.db.security_info)

        try:

            current_app.logger.debug("Generating access token")

            invokers_col = self.db.get_col_by_name(self.db.capif_invokers)

            current_app.logger.debug("Checking api invoker with id: " + access_token_req["client_id"])
            invoker =  invokers_col.find_one({"api_invoker_id": access_token_req["client_id"]})
            if invoker is None:
                client_id_error =  AccessTokenErr(error="invalid_client", error_description="Client Id not found")
                return make_response(object=client_id_error, status=400)


            if access_token_req["grant_type"] != "client_credentials":
                client_id_error =  AccessTokenErr(error="unsupported_grant_type", error_description="Invalid value for `grant_type` ({0}), must be one of ['client_credentials'] - 'grant_type'"
                .format(access_token_req["grant_type"]))
                return make_response(object=client_id_error, status=400)

            service_security = mycol.find_one({"api_invoker_id": security_id})
            if service_security is None:
                current_app.logger.error("Not found securoty context with id: " + security_id)
                return not_found_error(detail= security_context_not_found_detail, cause=api_invoker_no_context_cause)

            result = self.__check_scope(access_token_req["scope"], service_security)

            if result != None:
                return result

            expire_time = timedelta(minutes=10)
            now=datetime.now()

            claims = AccessTokenClaims(iss = access_token_req["client_id"], scope=access_token_req["scope"], exp=int((now+expire_time).timestamp()))
            access_token = create_access_token(identity = access_token_req["client_id"] , additional_claims=claims.to_dict())
            access_token_resp = AccessTokenRsp(access_token=access_token, token_type="Bearer", expires_in=int(expire_time.total_seconds()), scope=access_token_req["scope"])

            current_app.logger.debug("Created access token")

            res = make_response(object=access_token_resp, status=200)
            return res
        except Exception as e:
            exception = "An exception occurred in return token"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))


    def update_servicesecurity(self, api_invoker_id, service_security):
        mycol = self.db.get_col_by_name(self.db.security_info)
        try:

            current_app.logger.debug("Updating security context")
            result = self.__check_invoker(api_invoker_id)
            if result != None:
                return result

            old_object = mycol.find_one({"api_invoker_id": api_invoker_id})

            if old_object is None:
                current_app.logger.error("Service api not found with id: " + api_invoker_id)
                return not_found_error(detail="Service API not existing", cause="Not exist securiy information for this invoker")

            for service_instance in service_security.security_info:
                if service_instance.interface_details is not None:
                    security_methods = service_instance.interface_details.security_methods
                    pref_security_methods = service_instance.pref_security_methods
                    valid_security_method = set(security_methods) & set(pref_security_methods)
                    service_instance.sel_security_method = list(valid_security_method)[0]
                else:
                    capif_service_col = self.db.get_col_by_name(self.db.capif_service_col)
                    services_security_object = capif_service_col.find_one({self.filter_aef_id: service_instance.aef_id}, {"aef_profiles.security_methods.$":1})

                    if services_security_object is None:
                        current_app.logger.error("Service api with this aefId not found: " + service_instance.aef_id)
                        return not_found_error(detail="Service with this aefId not found", cause="Not found Service")

                    pref_security_methods = service_instance.pref_security_methods
                    valid_security_methods = [security_method for array_methods in services_security_object["aef_profiles"] for security_method in array_methods["security_methods"]]
                    valid_security_method = set(valid_security_methods) & set(pref_security_methods)
                    service_instance.sel_security_method = list(valid_security_method)[0]

            service_security = service_security.to_dict()
            service_security = clean_empty(service_security)

            result = mycol.find_one_and_update(old_object, {"$set":service_security}, projection={'_id': 0, "api_invoker_id":0},return_document=ReturnDocument.AFTER ,upsert=False)

            result = clean_empty(result)

            current_app.logger.debug("Updated security context")

            res= make_response(object=dict_to_camel_case(result), status=200)
            res.headers['Location'] = "https://${CAPIF_HOSTNAME}/capif-security/v1/trustedInvokers/" + str(
                api_invoker_id)
            return res
        except Exception as e:
            exception = "An exception occurred in update security info"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))


    def revoke_api_authorization(self, api_invoker_id, security_notification):

        mycol = self.db.get_col_by_name(self.db.security_info)

        try:

            current_app.logger.debug("Revoking security context")
            result = self.__check_invoker(api_invoker_id)
            if result != None:
                return result

            my_query = {'api_invoker_id': api_invoker_id}
            services_security_context = mycol.find_one(my_query)

            if services_security_context is None:
                current_app.logger.error(security_context_not_found_detail)
                return not_found_error(detail=security_context_not_found_detail, cause=api_invoker_no_context_cause)

            updated_security_context = services_security_context.copy()
            for context in services_security_context["security_info"]:
                index = services_security_context["security_info"].index(context)
                if security_notification.aef_id == context["aef_id"] or context["api_id"] in security_notification.api_ids:
                    updated_security_context["security_info"].pop(index)

            mycol.replace_one(my_query, updated_security_context)

            if len(updated_security_context["security_info"]) == 0:
                mycol.delete_many(my_query)

            self.notification.send_notification(services_security_context["notification_destination"], security_notification)

            current_app.logger.debug("Revoked security context")
            out= "Netapp with ID " + api_invoker_id + " was revoked by some APIs.", 204
            return make_response(out, status=204)

        except Exception as e:
            exception = "An exception occurred in revoke security auth"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))