import sys

import pymongo
import secrets
from flask import current_app, Flask, Response
import json

from ..db.db import MongoDatabse, ELKDatabase
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails


class LoggingInvocationOperations:

    def __init__(self):
        self.db = MongoDatabse()
        self.elastic = ELKDatabase()
        self.mimetype = 'application/json'

        es = self.elastic.get_connector()

        if 'capiflogs' not in es.indices.get_alias().keys():
            capif_logs_mapping = {
                "mappings": {
                    "properties": {
                        "logId": {"type": "text", "analyzer": "standard"},
                        "aefId": {"type": "text", "analyzer": "standard"},
                        "apiInvokerId": {"type": "text", "analyzer": "standard"},
                        "apiId": {"type": "text", "analyzer": "standard"},
                        "apiName": {"type": "text", "analyzer": "standard"},
                        "apiVersion": {"type": "text", "analyzer": "standard"},
                        "resourceName": {"type": "text", "analyzer": "standard"},
                        "uri": {"type": "text", "analyzer": "standard"},
                        "protocol": {"type": "text", "analyzer": "standard"},
                        "operation": {"type": "text", "analyzer": "standard"},
                        "result": {"type": "text", "analyzer": "standard"},
                        "invocationTime": {"type": "date", "format": "dd-MM-yyyy HH:mm:ss"},
                        "invocationLatency": {"type": "integer"},
                        "inputParameters": {"type": "text", "analyzer": "standard"},
                        "outputParameters": {"type": "text", "analyzer": "standard"},
                        "srcInterface": {
                            "properties": {
                                "ipv4Addr": {"type": "text", "analyzer": "standard"},
                                "ipv6Addr": {"type": "text", "analyzer": "standard"},
                                "port": {"type": "text", "analyzer": "standard"},
                                "securityMethods": {"type": "text", "analyzer": "standard"}
                            }
                        },
                        "destInterface": {
                            "properties": {
                                "ipv4Addr": {"type": "text", "analyzer": "standard"},
                                "ipv6Addr": {"type": "text", "analyzer": "standard"},
                                "port": {"type": "text", "analyzer": "standard"},
                                "securityMethods": {"type": "text", "analyzer": "standard"}
                            }
                        },
                        "fwdInterface": {"type": "text", "analyzer": "standard"},
                        "supportedFeatures": {"type": "text", "analyzer": "standard"}
                    }
                }
            }
            es.indices.create(index="capiflogs", body=capif_logs_mapping)


    def add_invocationlog(self, aef_id, invocationlog):

        mycol = self.db.get_col_by_name(self.db.invocation_logs)
        inv_col = self.db.get_col_by_name(self.db.invoker_details)
        prov_col = self.db.get_col_by_name(self.db.provider_details)
        users_col = self.db.get_col_by_name(self.db.capif_users)
        elk_connector = self.elastic.get_connector()

        try:
            aef_res = prov_col.find_one({'api_prov_dom_id': aef_id})
            invoker_res = inv_col.find_one({'api_invoker_id': invocationlog.api_invoker_id})

            if aef_res is None:
                prob = ProblemDetails(title="Unauthorized", status=401, detail="Exposer not existing",
                                    cause="Exposer id not found")
                return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype=self.mimetype)
            elif invoker_res is None:
                prob = ProblemDetails(title="Unauthorized", status=401, detail="Invoker not existing",
                                      cause="Invoker id not found")
                return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype=self.mimetype)
            else:
                ####### Implementation 1: Each Log entry is stored as different InvocationLog #######
                log_id = secrets.token_hex(15)
                invocationlog_copy = invocationlog.to_dict()
                invocationlog_copy2 = invocationlog.to_dict()
                del invocationlog_copy['logs']
                del invocationlog_copy2['logs']
                for i in range(0, len(invocationlog.logs)):
                    print(invocationlog.logs[i])
                    rec = dict()
                    rec['log_id'] = log_id
                    rec['logs'] = [invocationlog.logs[i].to_dict()]
                    rec.update(invocationlog_copy)
                    mycol.insert_one(rec)

                ####### Implementation 2: A Log array is stored as 1 InvocationLog #######
                # log_id = secrets.token_hex(15)
                # invocationlog.log_id = log_id
                # rec = dict()
                # rec['log_id'] = log_id
                # rec.update(invocationlog.to_dict())
                # mycol.insert_one(rec)

                ####### Implementation 3: A Log array is stored as different InvocationLog in Elasticsearch #######
                for i in range(0, len(invocationlog.logs)):
                    print(invocationlog.logs[i])
                    rec = dict()
                    rec['log_id'] = log_id
                    rec['logs'] = [invocationlog.logs[i].to_dict()]
                    rec.update(invocationlog_copy2)
                    elk_connector.index(index="capiflogs", body=rec)

                res = Response(json.dumps(invocationlog, cls=JSONEncoder), status=201, mimetype=self.mimetype)

                res.headers['Location'] = "http://localhost:8080/" + str(aef_id) + "/logs/" + str(log_id)
                return res

        except Exception as e:
            exception = "An exception occurred in add services::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)

