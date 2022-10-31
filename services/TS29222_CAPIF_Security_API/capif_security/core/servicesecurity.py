import sys

import pymongo
import secrets
import re
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
from ..util import dict_to_camel_case
import os

class SecurityOperations:

    def __init__(self):
        self.db = MongoDatabse()
        self.mimetype = 'application/json'

    def __check_invoker(self, api_invoker_id):
        invokers_col = self.db.get_col_by_name(self.db.capif_invokers)
        invoker =  invokers_col.find_one({"api_invoker_id": api_invoker_id})
        if invoker is None:
            prob = ProblemDetails(title="Not found", status=404, detail="Invoker not found",
                                cause="API Invoker not exists or invalid ID")
            return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype=self.mimetype)
        return None

    def __check_scope(self, scope, security_context):

        try:
            header = scope[0:4]
            if header != "3gpp":
                token_error = AccessTokenErr(error="invalid_scope", error_description="The first characters must be '3gpp'")
                return Response(json.dumps(token_error, cls=JSONEncoder), status=400, mimetype=self.mimetype)

            _, body = scope.split("#")

            capif_service_col = self.db.get_col_by_name(self.db.capif_service_col)
            security_info = security_context["security_info"]
            aef_security_context = [info["aef_id"] for info in security_info]

            groups = body.split(";")
            for group in groups:
                aef_id, api_names = group.split(":")
                if aef_id not in aef_security_context:
                    token_error = AccessTokenErr(error="invalid_scope", error_description="One of aef_id not belongs of your security context")
                    return Response(json.dumps(token_error, cls=JSONEncoder), status=400, mimetype=self.mimetype)
                api_names = api_names.split(",")
                for api_name in api_names:
                    service = capif_service_col.find_one({"$and": [{"api_name":api_name},{"aef_profiles.aef_id":aef_id}]})
                    if service is None:
                        token_error = AccessTokenErr(error="invalid_scope", error_description="One of the api names does not exist or is not associated with the aef id provided")
                        return Response(json.dumps(token_error, cls=JSONEncoder), status=400, mimetype=self.mimetype)

            return None

        except Exception as e:
            token_error = AccessTokenErr(error="invalid_scope", error_description="malformed scope")
            return Response(json.dumps(token_error, cls=JSONEncoder), status=400, mimetype=self.mimetype)

    def get_servicesecurity(self, api_invoker_id, authentication_info=True, authorization_info=True):

        mycol = self.db.get_col_by_name(self.db.security_info)

        try:

            result = self.__check_invoker(api_invoker_id)
            if result != None:
                return result
            else:
                services_security_object = mycol.find_one({"api_invoker_id": api_invoker_id}, {"_id":0, "api_invoker_id":0})

                if services_security_object is None:
                    prob = ProblemDetails(title="Not found", status=404, detail="Security context not found",
                                        cause="API Invoker has no security context")
                    return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype=self.mimetype)

                if not authentication_info:
                    for securityInfo_obj in services_security_object['security_info']:
                        del securityInfo_obj['authentication_info']
                if not authorization_info:
                    for securityInfo_obj in services_security_object['security_info']:
                        del securityInfo_obj['authorization_info']

                properyly_json= json.dumps(services_security_object, default=json_util.default)
                my_service_security = dict_to_camel_case(json.loads(properyly_json))
                res = Response(json.dumps(my_service_security, cls=JSONEncoder), status=200, mimetype=self.mimetype)
                return res
        except Exception as e:
            exception = "An exception occurred in get security info::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)


    def create_servicesecurity(self, api_invoker_id, service_security):

        mycol = self.db.get_col_by_name(self.db.security_info)

        try:
            result = self.__check_invoker(api_invoker_id)
            if result != None:
                return result

            if not re.match("^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$", service_security.notification_destination):

                prob = ProblemDetails(title="Malformed notidication destination", status=403, detail="Malformed notification destination param",
                                    cause="Bad URL Format")
                return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype=self.mimetype)

            services_security_object = mycol.find_one({"api_invoker_id": api_invoker_id})

            if services_security_object is not None:

                prob = ProblemDetails(title="Forbidden", status=403, detail="Security method already defined",
                                    cause="Identical AEF Profile IDs")
                return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype=self.mimetype)

            for service_instance in service_security.security_info:
                if service_instance.interface_details is not None:
                    security_methods = service_instance.interface_details.security_methods
                    pref_security_methods = service_instance.pref_security_methods
                    valid_security_method = set(security_methods) & set(pref_security_methods)
                    service_instance.sel_security_method = list(valid_security_method)[0]
                else:
                    capif_service_col = self.db.get_col_by_name(self.db.capif_service_col)
                    services_security_object = capif_service_col.find_one({"aef_profiles.aef_id": service_instance.aef_id}, {"aef_profiles.security_methods.$":1})

                    if services_security_object is None:
                        prob = ProblemDetails(title="Service Not found", status=404, detail="Service with this aefId not found",
                                cause="Not found Service")
                        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype=self.mimetype)

                    pref_security_methods = service_instance.pref_security_methods
                    valid_security_methods = [security_method for array_methods in services_security_object["aef_profiles"] for security_method in array_methods["security_methods"]]
                    valid_security_method = set(valid_security_methods) & set(pref_security_methods)
                    service_instance.sel_security_method = list(valid_security_method)[0]

            rec = dict()
            rec['api_invoker_id'] = api_invoker_id
            rec.update(service_security.to_dict())
            mycol.insert_one(rec)

            res = Response(json.dumps(service_security, cls=JSONEncoder), status=201, mimetype=self.mimetype)
            res.headers['Location'] = "https://{}/capif-security/v1/trustedInvokers/{}".format(os.getenv('CAPIF_HOSTNAME'),str(api_invoker_id))
            return res

        except Exception as e:
            exception = "An exception occurred in create security info::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)


    def delete_servicesecurity(self, api_invoker_id):

        mycol = self.db.get_col_by_name(self.db.security_info)

        try:
            result = self.__check_invoker(api_invoker_id)
            if result != None:
                return result
            else:
                myQuery = {'api_invoker_id': api_invoker_id}
                services_security_count = mycol.count_documents(myQuery)

                if services_security_count == 0:

                    prob = ProblemDetails(title="Not found", status=404, detail="Security context not found",
                                        cause="API Invoker has no security context")
                    return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype=self.mimetype)

                mycol.delete_many(myQuery)
                return "The security info of Netapp with Netapp ID " + api_invoker_id + " were deleted.", 204
        except Exception as e:
            exception = "An exception occurred in create security info::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)


    def return_token(self, security_id, access_token_req):

        mycol = self.db.get_col_by_name(self.db.security_info)

        try:

            result = self.__check_invoker(access_token_req["client_id"])
            if result != None:
                return result

            service_security = mycol.find_one({"api_invoker_id": security_id})
            if service_security is None:

                prob = AccessTokenErr(error="invalid_request", error_description="No Security Context for this API Invoker")
                return Response(json.dumps(prob, cls=JSONEncoder), status=400, mimetype=self.mimetype)
            else:

                result = self.__check_scope(access_token_req["scope"], service_security)

                if result != None:
                    return result

                expire_time = timedelta(minutes=10)
                now=datetime.now()

                claims = AccessTokenClaims(iss = access_token_req["client_id"], scope=access_token_req["scope"], exp=int((now+expire_time).timestamp()))
                access_token = create_access_token(identity = access_token_req["client_id"] , additional_claims=claims.to_dict())
                access_token_resp = AccessTokenRsp(access_token=access_token, token_type="bearer", expires_in=expire_time.total_seconds(), scope=access_token_req["scope"])

                res = Response(json.dumps(access_token_resp, cls=JSONEncoder), status=200, mimetype=self.mimetype)
                return res
        except Exception as e:
            exception = "An exception occurred in return token::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)


    def update_servicesecurity(self, api_invoker_id, service_security):
        mycol = self.db.get_col_by_name(self.db.security_info)
        try:
            result = self.__check_invoker(api_invoker_id)
            if result != None:
                return result

            old_object = mycol.find_one({"api_invoker_id": api_invoker_id})

            if old_object is None:

                prob = ProblemDetails(title="Not found", status=404, detail="Service API not existing",
                                    cause="Not exist securiy information for this invoker")
                return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype=self.mimetype)

            for service_instance in service_security.security_info:
                if service_instance.interface_details is not None:
                    security_methods = service_instance.interface_details.security_methods
                    pref_security_methods = service_instance.pref_security_methods
                    valid_security_method = set(security_methods) & set(pref_security_methods)
                    service_instance.sel_security_method = list(valid_security_method)[0]
                else:
                    capif_service_col = self.db.get_col_by_name(self.db.capif_service_col)
                    services_security_object = capif_service_col.find_one({"aef_profiles.aef_id": service_instance.aef_id}, {"aef_profiles.security_methods.$":1})

                    if services_security_object is None:
                        prob = ProblemDetails(title="Service Not found", status=404, detail="Service with this aefId not found",
                                cause="Not found Service")
                        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype=self.mimetype)


                    pref_security_methods = service_instance.pref_security_methods
                    valid_security_methods = [security_method for array_methods in services_security_object["aef_profiles"] for security_method in array_methods["security_methods"]]
                    valid_security_method = set(valid_security_methods) & set(pref_security_methods)
                    service_instance.sel_security_method = list(valid_security_method)[0]

            service_security = service_security.to_dict()
            service_security = {
                key: value for key, value in service_security.items() if value is not None
            }

            mycol.update_one(old_object, {"$set":service_security}, upsert=False)

            res = Response(json.dumps(service_security, cls=JSONEncoder), status=200, mimetype=self.mimetype)
            res.headers['Location'] = "https://${CAPIF_HOSTNAME}/capif-security/v1/trustedInvokers/" + str(
                api_invoker_id)
            return res
        except Exception as e:
            exception = "An exception occurred in update security info::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)


    def revoke_api_authorization(self, api_invoker_id, security_notification):

        mycol = self.db.get_col_by_name(self.db.security_info)
        invokers_col = self.db.get_col_by_name(self.db.capif_invokers)

        invoker =  invokers_col.find_one({"api_invoker_id": api_invoker_id})
        if invoker is None:

            prob = ProblemDetails(title="Not found", status=404, detail="Invoker not found",
                                cause="API Invoker not exists or invalid ID")
            return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype=self.mimetype)

        myQuery = {'api_invoker_id': api_invoker_id}
        services_security_count = mycol.count_documents(myQuery)

        if services_security_count == 0:

            prob = ProblemDetails(title="Not found", status=404, detail="Security context not found",
                                cause="API Invoker has no security context")
            return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype=self.mimetype)
        mycol.delete_many(myQuery)
        return "Netapp with ID " + api_invoker_id + " was revoked by some APIs.", 204