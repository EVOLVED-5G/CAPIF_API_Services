import sys

import pymongo
from flask import current_app, Flask, Response
import json
from ..db.db import MongoDatabse
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from bson import json_util


class DiscoverApisOperations:

    def __init__(self):
        self.db = MongoDatabse()
        self.mimetype = 'application/json'


    def get_discoveredapis(self, api_invoker_id, api_name, api_version, comm_type, protocol, aef_id,
                        data_format, api_cat, supported_features, api_supported_features):

        services = self.db.get_col_by_name(self.db.service_api_descriptions)
        invokers = self.db.get_col_by_name(self.db.invoker_col)

        try:
            invoker = invokers.find_one({"api_invoker_id": api_invoker_id})
            if invoker is None:

                prob = ProblemDetails(title="Forbidden", status=403, detail="API Invoker does not exist", cause="API Invoker id not found")
                return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype=self.mimetype)

            else:
                myParams = []
                myQuery = {}
                if api_name is not None:
                    myParams.append({"api_name": api_name})
                if api_version is not None:
                    myParams.append({"aef_profiles.0.versions.0.api_version": api_version})
                if comm_type is not None:
                    myParams.append({"aef_profiles.0.versions.0.resources.0.comm_type": comm_type})
                if protocol is not None:
                    myParams.append({"aef_profiles.0.protocol": protocol})
                if aef_id is not None:
                    myParams.append({"aef_profiles.0.aef_id": aef_id})
                if data_format is not None:
                    myParams.append({"aef_profiles.0.data_format": data_format})
                if api_cat is not None:
                    myParams.append({"service_api_category": api_cat})
                if supported_features is not None:
                    myParams.append({"supported_features": supported_features})
                if api_supported_features is not None:
                    myParams.append({"api_supp_feats": api_supported_features})
                if myParams:
                    myQuery = {"$and": myParams}

                discoved_apis = services.find(myQuery)
                json_docs = []
                for discoved_api in discoved_apis:
                    del discoved_api['_id']
                    del discoved_api['apf_id']
                    json_docs.append(discoved_api)

                res = Response(json.dumps(json_docs, default=json_util.default), status=200, mimetype=self.mimetype)
                return res

        except Exception as e:
            exception = "An exception occurred in discover services::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)

