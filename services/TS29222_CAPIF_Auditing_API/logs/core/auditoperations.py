import sys

from flask import current_app, Flask, Response
import json

from .resources import Resource
from bson import json_util
from .responses import bad_request_error, not_found_error, forbidden_error, internal_server_error, make_response


class AuditOperations (Resource):

    def get_logs(self, query_parameters):

        mycol = self.db.get_col_by_name(self.db.invocation_logs)

        current_app.logger.debug("Find invocation logs")

        try:

            my_params = []
            my_query = {}

            query_params_name = {
                                 "aef_id": "aef_id",
                                 "api_invoker_id": "api_invoker_id",
                                 "api_id": "logs.api_id",
                                 "api_name": "logs.api_name",
                                 "api_version": "logs.api_version",
                                 "protocol": "logs.protocol",
                                 "operation": "logs.operation",
                                 "result": "logs.result",
                                 "resource_name": "logs.resource_name",
                                 "supported_features": "supported_features"
                                }

            for param in query_parameters:
                if param in query_params_name and query_parameters[param] is not None:
                    my_params.append({query_params_name[param]: query_parameters[param]})

            if query_parameters["time_range_start"] is not None and query_parameters["time_range_end"] is not None:
                my_params.append({"logs.invocation_time": {'$gte': query_parameters["time_range_start"], '$lt': query_parameters["time_range_end"]}})
            elif query_parameters["time_range_start"] is not None:
                my_params.append({"logs.invocation_time": {'$gte': query_parameters["time_range_start"]}})
            elif query_parameters["time_range_end"] is not None:
                my_params.append({"logs.invocation_time": {'$lt': query_parameters["time_range_end"]}})

            if query_parameters["src_interface"] is not None:
                src_int_json = json.loads(query_parameters["src_interface"])
                ipv4_addr = src_int_json["ipv4Addr"]
                port = src_int_json["port"]
                security_methods = src_int_json["securityMethods"]
                my_params.append({"logs.src_interface.ipv4_addr": ipv4_addr, "logs.src_interface.port": port, "logs.src_interface.security_methods": security_methods})

            if query_parameters["dest_interface"] is not None:
                dest_int_json = json.loads(query_parameters["dest_interface"])
                ipv4_addr = dest_int_json["ipv4Addr"]
                port = dest_int_json["port"]
                security_methods = dest_int_json["securityMethods"]
                my_params.append({"logs.dest_interface.ipv4_addr": ipv4_addr, "logs.dest_interface.port": port, "logs.dest_interface.security_methods": security_methods})

            if my_params:
                my_query = {"$and": my_params}

            logs = mycol.find(my_query, {"_id":0})
            audit_logs = []
            for log in logs:
                audit_logs.append(log)

            res = make_response(object=audit_logs, status=200)
            current_app.logger.debug("Found invocation logs")
            return res

        except Exception as e:
            exception = "An exception occurred in audit"
            return internal_server_error(detail=exception, cause=str(e))

