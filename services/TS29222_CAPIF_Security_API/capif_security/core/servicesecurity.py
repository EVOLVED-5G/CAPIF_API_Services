import sys

import pymongo
import secrets
from flask import current_app, Flask, Response
from flask_jwt_extended import create_access_token
import json
from ..db.db import MongoDatabse
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from ..models.access_token_rsp import AccessTokenRsp
from ..models.access_token_claims import AccessTokenClaims
from ..utils.jws_generate import sign_token
from bson import json_util
import requests
from ..models.access_token_err import AccessTokenErr
from ..models.service_security import ServiceSecurity
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
            return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype='application/json')
        return None

    def get_servicesecurity(self, api_invoker_id, authentication_info=True, authorization_info=True):

        mycol = self.db.get_col_by_name(self.db.security_info)

        try:

            result = self.__check_invoker(api_invoker_id)
            if result != None:
                return result
            else:
                services_security_object = mycol.find_one({"api_invoker_id": api_invoker_id})

                if services_security_object is None:
                    prob = ProblemDetails(title="Not found", status=404, detail="Security context not found",
                                        cause="API Invoker has no security context")
                    return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype='application/json')

                del services_security_object['_id']
                del services_security_object['api_invoker_id']
                if not authentication_info:
                    for securityInfo_obj in services_security_object['security_info']:
                        del securityInfo_obj['authentication_info']
                if not authorization_info:
                    for securityInfo_obj in services_security_object['security_info']:
                        del securityInfo_obj['authorization_info']


                res = Response(json.dumps(services_security_object, cls=JSONEncoder), status=200, mimetype='application/json')
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

            else:
                services_security_object = mycol.find_one({"api_invoker_id": api_invoker_id})

                if services_security_object is not None:

                    prob = ProblemDetails(title="Forbidden", status=403, detail="Security method already defined",
                                        cause="Identical AEF Profile IDs")
                    return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')
                else:

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
                                return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')


                            pref_security_methods = service_instance.pref_security_methods
                            valid_security_methods = [security_method for array_methods in services_security_object["aef_profiles"] for security_method in array_methods["security_methods"]]
                            valid_security_method = set(valid_security_methods) & set(pref_security_methods)
                            service_instance.sel_security_method = list(valid_security_method)[0]

                    rec = dict()
                    rec['api_invoker_id'] = api_invoker_id
                    rec.update(service_security.to_dict())
                    mycol.insert_one(rec)

                    res = Response(json.dumps(service_security, cls=JSONEncoder), status=201, mimetype='application/json')
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
                    return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype='application/json')

                mycol.delete_many(myQuery)
                return "The security info of Netapp with Netapp ID " + api_invoker_id + " were deleted.", 204
        except Exception as e:
            exception = "An exception occurred in create security info::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)


    def return_token(self, security_id, access_token_req):

        print(access_token_req, file=sys.stderr)
        
        mycol = self.db.get_col_by_name(self.db.security_info)

        try:

            result = self.__check_invoker(access_token_req["client_id"])
            if result != None:
                return result

            service_security = mycol.find_one({"api_invoker_id": security_id})
            if service_security is None:

                prob = AccessTokenErr(error="invalid_request", error_description="No Security Context for this API Invoker")
                return Response(json.dumps(prob, cls=JSONEncoder), status=400, mimetype='application/json')
            else:
                #we need to check scope
                if access_token_req["scope"] is None or access_token_req["scope"]== " ":
                    access_token_req["scope"] = "3gpp#"
                claims = AccessTokenClaims(iss = access_token_req["client_id"], scope=access_token_req["scope"], exp=691200)
                access_token = sign_token(claims.to_dict())
                #access_token = create_access_token(identity=(request_token_obj["client_id"] + " " + request_token_obj["scope"] + " " + "691200"))
                access_token_resp = AccessTokenRsp(access_token=access_token, token_type="bearer", expires_in=691200, scope=access_token_req["scope"])

                res = Response(json.dumps(access_token_resp, cls=JSONEncoder), status=200, mimetype='application/json')
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

            else:
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
                            return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')


                        pref_security_methods = service_instance.pref_security_methods
                        valid_security_methods = [security_method for array_methods in services_security_object["aef_profiles"] for security_method in array_methods["security_methods"]]
                        valid_security_method = set(valid_security_methods) & set(pref_security_methods)
                        service_instance.sel_security_method = list(valid_security_method)[0]

                service_security = service_security.to_dict()
                service_security = {
                    key: value for key, value in service_security.items() if value is not None
                }

                mycol.update_one(old_object, {"$set":service_security}, upsert=False)

                res = Response(json.dumps(service_security, cls=JSONEncoder), status=200, mimetype='application/json')
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
            return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype='application/json')
        else:
            myQuery = {'api_invoker_id': api_invoker_id}
            services_security_count = mycol.count_documents(myQuery)

            if services_security_count == 0:

                prob = ProblemDetails(title="Not found", status=404, detail="Security context not found",
                                    cause="API Invoker has no security context")
                return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype='application/json')
            mycol.delete_many(myQuery)
            return "Netapp with ID " + api_invoker_id + " was revoked by some APIs.", 204