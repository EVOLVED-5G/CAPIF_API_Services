import sys
import os
import pymongo
import secrets
from flask import current_app, Flask, Response
import json

from ..db.db import MongoDatabse
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from .resources import Resource
from .responses import bad_request_error, internal_server_error, forbidden_error, not_found_error, unauthorized_error, make_response


class LoggingInvocationOperations(Resource):

    def __check_aef(self, aef_id):
        prov_col = self.db.get_col_by_name(self.db.provider_details)

        current_app.logger.debug("Checking aef id")
        # aef_res = prov_col.find_one({'api_prov_dom_id': aef_id})
        aef_res = prov_col.find_one({'api_prov_funcs': {'$elemMatch': {'api_prov_func_role': 'AEF', 'api_prov_func_id': aef_id}}})

        if aef_res is None:
            current_app.logger.error("Exposer not exist")
            return not_found_error(detail="Exposer not exist", cause="Exposer id not found")

        return None

    def __check_invoker(self, invoker_id):
        inv_col = self.db.get_col_by_name(self.db.invoker_details)

        current_app.logger.debug("Checking invoker id")
        invoker_res = inv_col.find_one({'api_invoker_id': invoker_id})

        if invoker_res is None:
            current_app.logger.error("Invoker not exist")
            return not_found_error(detail="Invoker not exist", cause="Invoker id not found")

        return None

    def __check_service_apis(self, api_id, api_name):
        serv_apis = self.db.get_col_by_name(self.db.service_apis)

        current_app.logger.debug("Checking service apis")
        services_api_res = serv_apis.find_one({"$and": [{'api_id': api_id}, {'api_name': api_name}]})

        if services_api_res is None:
            detail = "Service API not exist"
            cause = "Service API with id {} and name {} not found".format(api_id, api_name)
            current_app.logger.error(detail)
            return not_found_error(detail=detail, cause=cause)

        return None

    def add_invocationlog(self, aef_id, invocationlog):

        mycol = self.db.get_col_by_name(self.db.invocation_logs)

        try:
            current_app.logger.debug("Adding invocation logs")
            result = self.__check_aef(aef_id)

            if result is not None:
                return result

            result = self.__check_invoker(invocationlog.api_invoker_id)

            if result is not None:
                return result

            for i in range(0, len(invocationlog.logs)):
                result = self.__check_service_apis(invocationlog.logs[i].api_id, invocationlog.logs[i].api_name)

                if result is not None:
                    return result

            log_id = secrets.token_hex(15)
            rec = dict()
            rec['log_id'] = log_id
            rec.update(invocationlog.to_dict())
            mycol.insert_one(rec)

            current_app.logger.debug("Invocation Logs inserted in database")
            res = make_response(object=invocationlog, status=201)
            res.headers['Location'] = "https://{}/api-invocation-logs/v1/{}/logs/{}".format(os.getenv('CAPIF_HOSTNAME'), str(aef_id), str(log_id))
            return res

        except Exception as e:
            exception = "An exception occurred in inserting invovation logs"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))

