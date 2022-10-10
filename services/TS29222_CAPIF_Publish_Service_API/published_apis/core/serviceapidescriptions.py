import sys

import pymongo
import secrets
from flask import current_app, Flask, Response
import json

from pymongo import response
from ..db.db import MongoDatabse
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from bson import json_util




class PublishServiceOperations:

    def __init__(self):
        self.db = MongoDatabse()
        self.mimetype = 'application/json'

    def check_apf(self, apf_id):
        providers_col = self.db.get_col_by_name(self.db.capif_provider_col)
        try:

            provider = providers_col.find_one({"api_prov_funcs.api_prov_func_id": apf_id})

            if provider is None:
                prob = ProblemDetails(title="Unauthorized", status=401, detail="Publisher not existing",
                                    cause="Publisher id not found")
                return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype=self.mimetype)

            list_apf_ids =  [func["api_prov_func_id"] for func in provider["api_prov_funcs"] if func["api_prov_func_role"] == "APF"]
            if apf_id not in list_apf_ids:
                 prob = ProblemDetails(title="Unauthorized", status=401, detail="You are not a publisher",
                                    cause="This API is only available for publishers")
                 return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype=self.mimetype)

            return None
        except Exception as e:
            return e

    def get_serviceapis(self, apf_id):

        mycol = self.db.get_col_by_name(self.db.service_api_descriptions)

        try:

            result = self.check_apf(apf_id)

            if result != None:
                return result

            service = mycol.find({"apf_id": apf_id})
            if service is None:
                prob = ProblemDetails(title="Services not exist", status=404, detail="Not exist published services for this apf_id",
                                    cause="Not exist service with this apf_id")
                return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype=self.mimetype)
            else:
                json_docs = []
                for serviceapi in service:
                    del serviceapi['apf_id']
                    del serviceapi['_id']
                    json_docs.append(serviceapi)

                res = Response(json.dumps(json_docs, default=json_util.default), status=200, mimetype=self.mimetype)
                return res

        except Exception as e:
            exception = "An exception occurred in get services::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)



    def add_serviceapidescription(self, apf_id, serviceapidescription):

        mycol = self.db.get_col_by_name(self.db.service_api_descriptions)
        providers_col = self.db.get_col_by_name(self.db.capif_provider_col)

        try:
            provider = providers_col.find_one({"api_prov_funcs.api_prov_func_id": apf_id})

            if provider is None:
                prob = ProblemDetails(title="Unauthorized", status=401, detail="Publisher not existing",
                                    cause="Publisher id not found")
                return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype=self.mimetype)

            list_apf_ids =  [func["api_prov_func_id"] for func in provider["api_prov_funcs"] if func["api_prov_func_role"] == "APF"]
            if apf_id not in list_apf_ids:
                 prob = ProblemDetails(title="Unauthorized", status=401, detail="You are not a publisher",
                                    cause="This API is only available for publishers")
                 return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype=self.mimetype)

            service = mycol.find_one({"apf_id": apf_id})
            if service is not None:
                prob = ProblemDetails(title="Service exist", status=409, detail="Already registered service with same apf id",
                                    cause="Found service with same aef id")
                return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype=self.mimetype)

            else:
                list_aef_ids = [func["api_prov_func_id"] for func in provider["api_prov_funcs"] if func["api_prov_func_role"] == "AEF"]
                for aef_profile in serviceapidescription.aef_profiles:
                    if aef_profile.aef_id not in list_aef_ids:
                        prob = ProblemDetails(title="Aef Id not exist", status=404, detail="Not exist aef with these id",
                                    cause="aef id not exist")
                        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype=self.mimetype)

                api_id = secrets.token_hex(15)
                serviceapidescription.api_id = api_id
                rec = dict()
                rec['apf_id'] = apf_id
                rec.update(serviceapidescription.to_dict())
                mycol.insert_one(rec)

                res = Response(json.dumps(serviceapidescription, cls=JSONEncoder), status=201, mimetype=self.mimetype)

                res.headers['Location'] = "http://localhost:8080/published-apis/v1/" + str(apf_id) + "/service-apis/" + str(api_id)
                return res

        except Exception as e:
            exception = "An exception occurred in add services::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)



    def get_one_serviceapi(self, service_api_id, apf_id):

        mycol = self.db.get_col_by_name(self.db.service_api_descriptions)

        try:
            result = self.check_apf(apf_id)

            if result != None:
                return result

            myQuery = {'apf_id': apf_id, 'api_id': service_api_id}
            service_api = mycol.find_one(myQuery)
            print(service_api)
            sys.stdin.flush()
            if service_api is None:
                prob = ProblemDetails(title="Not Found", status=404, detail="Service API not found",
                                    cause="No Service with specific credentials exists")
                return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype=self.mimetype)

            else:
                del service_api['apf_id']
                del service_api['_id']

                res = Response(json.dumps(service_api, default=json_util.default), status=200, mimetype=self.mimetype)
                return res
        except Exception as e:
            exception = "An exception occurred in get one service::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)



    def delete_serviceapidescription(self, service_api_id, apf_id):

        mycol = self.db.get_col_by_name(self.db.service_api_descriptions)

        try:

            result = self.check_apf(apf_id)

            if result != None:
                return result

            myQuery = {'apf_id': apf_id, 'api_id': service_api_id}
            serviceapidescription = mycol.find_one(myQuery)

            if serviceapidescription is None:

                prob = ProblemDetails(title="Unauthorized", status=404, detail="Service API not existing",
                                    cause="Service API id not found")
                return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype=self.mimetype)

            else:
                mycol.delete_one(myQuery)
                return Response(json.dumps(serviceapidescription, default=str, cls=JSONEncoder), status=204, mimetype=self.mimetype)
        except Exception as e:
            exception = "An exception occurred in delete service::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)



    def update_serviceapidescription(self, service_api_id, apf_id, service_api_description):

        mycol = self.db.get_col_by_name(self.db.service_api_descriptions)

        try:

            result = self.check_apf(apf_id)

            if result != None:
                return result

            myQuery = {'apf_id': apf_id, 'api_id': service_api_id}
            serviceapidescription = mycol.find_one(myQuery)

            if serviceapidescription is None:

                prob = ProblemDetails(title="Unauthorized", status=404, detail="Service API not existing",
                                    cause="Service API id not found")
                return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype=self.mimetype)

            else:

                service_api_description = service_api_description.to_dict()
                service_api_description = {
                    key: value for key, value in service_api_description.items() if value is not None
                }

                mycol.update_one(serviceapidescription, {"$set":service_api_description}, upsert=False)
                response = Response(json.dumps(service_api_description, default=str,cls=JSONEncoder), status=200, mimetype=self.mimetype)

                return response
        except Exception as e:
            exception = "An exception occurred in update service::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)

