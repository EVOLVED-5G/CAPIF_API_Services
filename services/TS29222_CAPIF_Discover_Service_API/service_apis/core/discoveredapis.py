import sys

import pymongo
from flask import current_app, Flask, Response
import json
from service_apis.core.responses import internal_server_error, forbidden_error ,make_response, not_found_error
from service_apis.db.db import MongoDatabse
from service_apis.encoder import JSONEncoder
from service_apis.models.problem_details import ProblemDetails
from service_apis.models.service_api_description import ServiceAPIDescription
from service_apis.models.discovered_apis import DiscoveredAPIs
from service_apis.util import dict_to_camel_case
from service_apis.core.resources import Resource
from bson import json_util



class DiscoverApisOperations(Resource):

    def get_discoveredapis(self, api_invoker_id, api_name, api_version, comm_type, protocol, aef_id,
                        data_format, api_cat, supported_features, api_supported_features):

        services = self.db.get_col_by_name(self.db.service_api_descriptions)
        invokers = self.db.get_col_by_name(self.db.invoker_col)

        current_app.logger.debug("Discovering services apis")

        try:
            invoker = invokers.find_one({"api_invoker_id": api_invoker_id})
            if invoker is None:
                current_app.logger.error("Api invoker not found in database")
                return not_found_error(detail="API Invoker does not exist", cause="API Invoker id not found")

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

            discoved_apis = services.find(myQuery, {"_id":0, "apf_id":0})
            json_docs = []
            for discoved_api in discoved_apis:

                properyly_json= json.dumps(discoved_api, default=json_util.default)
                my_api = dict_to_camel_case(json.loads(properyly_json))
                json_docs.append(my_api)

            apis_discoveres = DiscoveredAPIs(service_api_descriptions=json_docs)
            res = make_response(object=apis_discoveres, status=200)
            current_app.logger.debug("Discovered APIs")
            return res

        except Exception as e:
            exception = "An exception occurred in discover services"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))

