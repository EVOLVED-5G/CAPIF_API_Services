import sys

from flask import current_app, Flask, Response
import json

from ..db.db import MongoDatabse
from ..encoder import JSONEncoder
from bson import json_util
from ..models.protocol import Protocol


class AuditOperations:

    def __init__(self):
        self.db = MongoDatabse()
        self.mimetype = 'application/json'

    def get_logs(self, aef_id, api_invoker_id, time_range_start, time_range_end, api_id, api_name, api_version, protocol, operation, result, resource_name, src_interface, dest_interface, supported_features):

        mycol = self.db.get_col_by_name(self.db.invocation_logs)
        users_col = self.db.get_col_by_name(self.db.capif_users)

        try:
            myParams = []
            myQuery = {}
            if aef_id is not None:
                myParams.append({"aef_id": aef_id})

            if api_invoker_id is not None:
                myParams.append({"api_invoker_id": api_invoker_id})

            if time_range_start is not None and time_range_end is not None:
                myParams.append({"logs.invocation_time": {'$gte': time_range_start, '$lt': time_range_end}})
            elif time_range_start is not None:
                myParams.append({"logs.invocation_time": {'$gte': time_range_start}})
            elif time_range_end is not None:
                myParams.append({"logs.invocation_time": {'$lt': time_range_end}})

            if api_id is not None:
                myParams.append({"logs.api_id": api_id})

            if api_name is not None:
                myParams.append({"logs.api_name": api_name})

            if api_version is not None:
                myParams.append({"logs.api_version": api_version})

            if protocol is not None:
                myParams.append({"logs.protocol": protocol})

            if operation is not None:
                myParams.append({"logs.operation": operation})

            if result is not None:
                myParams.append({"logs.result": result})

            if resource_name is not None:
                myParams.append({"logs.resource_name": resource_name})

            if src_interface is not None:
                src_int_json = json.loads(src_interface)
                ipv4Addr = src_int_json["ipv4Addr"]
                port = src_int_json["port"]
                security_methods = src_int_json["securityMethods"]
                myParams.append({"logs.src_interface.ipv4_addr": ipv4Addr, "logs.src_interface.port": port, "logs.src_interface.security_methods": security_methods})

            if dest_interface is not None:
                dest_int_json = json.loads(dest_interface)
                ipv4Addr = dest_int_json["ipv4Addr"]
                port = dest_int_json["port"]
                security_methods = dest_int_json["securityMethods"]
                myParams.append({"logs.dest_interface.ipv4_addr": ipv4Addr, "logs.dest_interface.port": port, "logs.dest_interface.security_methods": security_methods})

            if supported_features is not None:
                myParams.append({"supported_features": supported_features})

            if myParams:
                myQuery = {"$and": myParams}

            logs = mycol.find(myQuery, {"_id":0})
            json_docs = []
            for log in logs:
                json_docs.append(log)

            res = Response(json.dumps(json_docs, default=json_util.default), status=200, mimetype=self.mimetype)
            return res

        except Exception as e:
            exception = "An exception occurred in add services::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)

