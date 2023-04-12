import sys

from flask import current_app, Flask, Response
import json
import sys
from datetime import datetime
from .resources import Resource
from bson import json_util
from ..util import dict_to_camel_case, clean_empty
from .responses import bad_request_error, not_found_error, forbidden_error, internal_server_error, make_response
from ..models.invocation_log import InvocationLog


class AuditOperations (Resource):

    def get_logs(self, query_parameters):

        mycol = self.db.get_col_by_name(self.db.invocation_logs)

        current_app.logger.debug("Find invocation logs")

        try:
            result = mycol.find_one({'aef_id': query_parameters['aef_id'], 'api_invoker_id': query_parameters['api_invoker_id']}, {"_id": 0})

            if result is None:
                return not_found_error(detail="aefId or/and apiInvokerId do not match any InvocationLogs", cause="No log invocations found")

            logs = result['logs'].copy()

            query_params = dict((k,v) for k,v in query_parameters.items() if v is not None and k != 'aef_id' and k != 'api_invoker_id')

            for log in logs:

                for param in query_params:
                    if param == 'time_range_start':
                        if query_params[param] > log['invocation_time'].astimezone(query_params[param].tzinfo):
                            result['logs'].remove(log)
                            break
                    elif param == 'time_range_end':
                        if query_params[param] < log['invocation_time'].astimezone(query_params[param].tzinfo):
                            result['logs'].remove(log)
                            break
                    elif param == 'src_interface' or param == 'dest_interface':
                        interface = json.loads(query_params[param])
                        if 'security_methods' not in interface:
                            return bad_request_error(detail="security_methods is mandatory",
                                                     cause="security_methods parameter missing", invalid_params=[
                                    {"param": "security_methods", "reason": "missing"}])
                        for key in interface:
                            if log[param][key] != interface[key]:
                                result['logs'].remove(log)
                                break
                    elif log[param] != query_params[param]:
                        result['logs'].remove(log)
                        break

            if not result['logs']:
                return not_found_error(detail="Parameters do not match any log entry", cause="No logs found")


            result = dict_to_camel_case(clean_empty(result))
            invocation_log = InvocationLog(result['aefId'], result['apiInvokerId'], result['logs'],
                                           result['supportedFeatures'])
            res = make_response(object=invocation_log, status=200)
            current_app.logger.debug("Found invocation logs")
            return res

        except Exception as e:
            exception = "An exception occurred in audit"
            return internal_server_error(detail=exception, cause=str(e))

