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


    def get_serviceapis(self, apf_id):

        mycol = self.db.get_col_by_name(self.db.service_api_descriptions)
        users_col = self.db.get_col_by_name(self.db.capif_users)

        try:

            apf_res = users_col.find_one({'_id': apf_id})
            if apf_res is None:

                prob = ProblemDetails(title="Unauthorized", status=401, detail="Exposer not existing",
                                    cause="Exposer id not found")
                return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype=self.mimetype)

            else:
                myQuery = {'apf_id': apf_id}
                service_apis = mycol.find(myQuery)
                json_docs = []
                for serviceapi in service_apis:
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
        users_col = self.db.get_col_by_name(self.db.capif_users)

        try:
            apf_res = users_col.find_one({'_id': apf_id})

            if apf_res is None:
                prob = ProblemDetails(title="Unauthorized", status=401, detail="Exposer not existing",
                                    cause="Exposer id not found")
                return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype=self.mimetype)

            else:
                myParams = [{"api_name": serviceapidescription.api_name}]
                for i in range(0,len(serviceapidescription.aef_profiles)):
                    myParams.append({"aef_profiles."+str(i)+".aef_id": serviceapidescription.aef_profiles[i].aef_id})
                myQuery = {"$and": myParams}
                res = mycol.find_one(myQuery)
                if res is not None:

                    prob = ProblemDetails(title="Forbidden", status=403, detail="Service already published",
                                        cause="Identical API name and AEF Profile IDs")
                    return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype=self.mimetype)

                else:
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
        users_col = self.db.get_col_by_name(self.db.capif_users)

        try:
            apf_res = users_col.find_one({'_id': apf_id})
            if apf_res is None:
                prob = ProblemDetails(title="Unauthorized", status=401, detail="Exposer not existing",
                                    cause="Exposer id not found")
                return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype=self.mimetype)

            else:
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
        users_col = self.db.get_col_by_name(self.db.capif_users)

        try:
            apf_res = users_col.find_one({'_id': apf_id})

            if apf_res is None:

                prob = ProblemDetails(title="Unauthorized", status=401, detail="Exposer not existing",
                                        cause="Exposer id not found")
                return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype=self.mimetype)


            else:
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
        users_col = self.db.get_col_by_name(self.db.capif_users)

        try:
            apf_res = users_col.find_one({'_id': apf_id})

            if apf_res is None:

                prob = ProblemDetails(title="Unauthorized", status=401, detail="Exposer not existing",
                                        cause="Exposer id not found")
                return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype=self.mimetype)

            else:

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

