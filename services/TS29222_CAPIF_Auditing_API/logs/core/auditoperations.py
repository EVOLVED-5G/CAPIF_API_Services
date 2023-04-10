import sys

from flask import current_app, Flask, Response
import json
import sys
from datetime import datetime
from .resources import Resource
from bson import json_util
from ..util import dict_to_camel_case, clean_empty
from .responses import bad_request_error, not_found_error, forbidden_error, internal_server_error, make_response


class AuditOperations (Resource):

    def get_logs(self, query_parameters):

        mycol = self.db.get_col_by_name(self.db.invocation_logs)

        current_app.logger.debug("Find invocation logs")

        try:

            my_params = []
            my_query = {}

            if 'aef_id' not in query_parameters or 'api_invoker_id' not in query_parameters:
                return bad_request_error(detail="aef_id and api_invoker_id parameters are mandatory", cause="Mandatory parameters missing", invalid_params=[
                    {"param": "aef_id or api_invoker_id", "reason": "missing"}])

            result_test = mycol.find_one({'aef_id': query_parameters['aef_id'], 'api_invoker_id': query_parameters['api_invoker_id']}, {"_id": 0})

            if result_test is None:
                return not_found_error(detail="aefId or/and apiInvokerId do not match any InvocationLogs", cause="No log invocations found")

            logs = result_test['logs'].copy()

            for log in logs:
                if query_parameters['api_id'] is not None:
                    if log['api_id'] != query_parameters['api_id']:
                        result_test['logs'].remove(log)
                        continue

                if query_parameters['api_name'] is not None:
                    if log['api_name'] != query_parameters['api_name']:
                        result_test['logs'].remove(log)
                        continue

                if query_parameters['api_version'] is not None:
                    if log['api_version'] != query_parameters['api_version']:
                        result_test['logs'].remove(log)
                        continue

                if query_parameters['resource_name'] is not None:
                    if log['resource_name'] != query_parameters['resource_name']:
                        result_test['logs'].remove(log)
                        continue

                if query_parameters['protocol'] is not None:
                    if log['protocol'] != query_parameters['protocol']:
                        result_test['logs'].remove(log)
                        continue

                if query_parameters['operation'] is not None:
                    if log['operation'] != query_parameters['operation']:
                        result_test['logs'].remove(log)
                        continue

                if query_parameters['result'] is not None:
                    if log['result'] != query_parameters['result']:
                        result_test['logs'].remove(log)
                        continue

                if query_parameters['supported_features'] is not None:
                    if log['supported_features'] != query_parameters['supported_features']:
                        result_test['logs'].remove(log)
                        continue

                if query_parameters["time_range_start"] is not None:
                    if query_parameters["time_range_start"] > log['invocation_time'].astimezone(query_parameters["time_range_start"].tzinfo):
                        result_test['logs'].remove(log)
                        continue

                if query_parameters["time_range_end"] is not None:
                    if query_parameters["time_range_end"] < log['invocation_time'].astimezone(query_parameters["time_range_end"].tzinfo):
                        result_test['logs'].remove(log)
                        continue

                if query_parameters['src_interface'] is not None:
                    src_int = json.loads(query_parameters['src_interface'])
                    if 'securityMethods' not in src_int:
                        return bad_request_error(detail="securityMethods is mandatory",
                                                 cause="securityMethods parameter missing", invalid_params=[
                                {"param": "securityMethods", "reason": "missing"}])
                    if log['src_interface']['security_methods'] != src_int['securityMethods']:
                        result_test['logs'].remove(log)
                        continue
                    if 'ipv4Addr' in src_int:
                        if log['src_interface']['ipv4_addr'] != src_int['ipv4Addr']:
                            result_test['logs'].remove(log)
                            continue
                    if 'port' in src_int:
                        if log['src_interface']['port'] != src_int['port']:
                            result_test['logs'].remove(log)
                            continue
                    if 'ipv6Addr' in src_int:
                        if log['src_interface']['ipv6_addr'] != src_int['ipv6_addr']:
                            result_test['logs'].remove(log)
                            continue

                if query_parameters['dest_interface'] is not None:
                    dest_int = json.loads(query_parameters['dest_interface'])
                    if 'securityMethods' not in dest_int:
                        return bad_request_error(detail="securityMethods is mandatory",
                                                 cause="securityMethods parameter missing", invalid_params=[
                                {"param": "securityMethods", "reason": "missing"}])
                    if log['dest_interface']['security_methods'] != dest_int['securityMethods']:
                        result_test['logs'].remove(log)
                        continue
                    if 'ipv4Addr' in dest_int:
                        if log['dest_interface']['ipv4_addr'] != dest_int['ipv4Addr']:
                            result_test['logs'].remove(log)
                            continue
                    if 'port' in dest_int:
                        if log['dest_interface']['port'] != dest_int['port']:
                            result_test['logs'].remove(log)
                            continue
                    if 'ipv6Addr' in dest_int:
                        if log['dest_interface']['ipv6_addr'] != dest_int['ipv6_addr']:
                            result_test['logs'].remove(log)
                            continue

            if not result_test['logs']:
                return not_found_error(detail="Parameters do not match any log entry", cause="No logs found")

            res = make_response(object=dict_to_camel_case(result_test), status=200)
            current_app.logger.debug("Found invocation logs")
            return res

        except Exception as e:
            exception = "An exception occurred in audit"
            return internal_server_error(detail=exception, cause=str(e))

