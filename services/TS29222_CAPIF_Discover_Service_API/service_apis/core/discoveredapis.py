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
from service_apis.util import dict_to_camel_case, clean_empty
from service_apis.core.resources import Resource
from bson import json_util



class DiscoverApisOperations(Resource):

    def get_discoveredapis(self, api_invoker_id, query_params):

        services = self.db.get_col_by_name(self.db.service_api_descriptions)
        invokers = self.db.get_col_by_name(self.db.invoker_col)

        current_app.logger.debug("Discovering services apis by: " + api_invoker_id)

        try:
            invoker = invokers.find_one({"api_invoker_id": api_invoker_id})
            if invoker is None:
                current_app.logger.error("Api invoker not found in database")
                return not_found_error(detail="API Invoker does not exist", cause="API Invoker id not found")

            my_params = []
            my_query = {}
            quey_params_name = {"api_name":"api_name", "api_version":"aef_profiles.0.versions.0.api_version", "comm_type":"aef_profiles.0.versions.0.resources.0.comm_type", 
            "protocol":"aef_profiles.0.protocol", "aef_id":"aef_profiles.0.aef_id", "data_format":"aef_profiles.0.data_format", 
            "api_cat":"service_api_category", "supported_features":"supported_features", "api_supported_features":"api_supp_feats"}

            for param in query_params:
                if query_params[param] is not None:
                    my_params.append({quey_params_name[param]: query_params[param]})

            if my_params:
                my_query = {"$and": my_params}

            discoved_apis = services.find(my_query, {"_id":0, "apf_id":0})
            json_docs = []
            for discoved_api in discoved_apis:
                my_api = dict_to_camel_case(discoved_api)
                my_api = clean_empty(my_api)
                json_docs.append(my_api)

            if len(json_docs) == 0:
                return not_found_error(detail="API Invoker " + api_invoker_id + " has no API Published that accomplish filter conditions", cause="No API Published accomplish filter conditions")

            apis_discoveres = DiscoveredAPIs(service_api_descriptions=json_docs)
            res = make_response(object=apis_discoveres, status=200)
            current_app.logger.debug("Discovered APIs by: " + api_invoker_id)
            return res

        except Exception as e:
            exception = "An exception occurred in discover services"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))

