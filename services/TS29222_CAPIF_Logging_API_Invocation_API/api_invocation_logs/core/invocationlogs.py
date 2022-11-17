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
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
import time


class LoggingInvocationOperations:

    def __init__(self):
        self.db = MongoDatabse()
        self.mimetype = 'application/json'
        # self.es = Elasticsearch(hosts=['http://elasticsearch:9200'], basic_auth=('elastic', 'changeme'), retry_on_timeout=True)
        #
        # for _ in range(100):
        #     try:
        #         # make sure the cluster is available
        #         self.es.cluster.health(wait_for_status="yellow")
        #     except ConnectionError:
        #         time.sleep(2)

        self.es = Elasticsearch(
            hosts=['http://elasticsearch:9200'],
            basic_auth=('elastic', 'changeme'),
            retry_on_timeout=True
        )
        mappings = {
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
        self.es.indices.create(index="capiflogs", mappings=mappings)

    def add_invocationlog(self, aef_id, invocationlog):

        mycol = self.db.get_col_by_name(self.db.invocation_logs)
        inv_col = self.db.get_col_by_name(self.db.invoker_details)
        prov_col = self.db.get_col_by_name(self.db.provider_details)
        users_col = self.db.get_col_by_name(self.db.capif_users)

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
                # myParams = [{"api_name": serviceapidescription.api_name}]
                # for i in range(0,len(serviceapidescription.aef_profiles)):
                #     myParams.append({"aef_profiles."+str(i)+".aef_id": serviceapidescription.aef_profiles[i].aef_id})
                # myQuery = {"$and": myParams}
                # res = mycol.find_one(myQuery)
                # if res is not None:
                #
                #     prob = ProblemDetails(title="Forbidden", status=403, detail="Service already published",
                #                         cause="Identical API name and AEF Profile IDs")
                #     return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype=self.mimetype)
                #
                # else:

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
                    # doc = dict()
                    # doc['logId'] = secrets.token_hex(15)
                    # doc['aefId'] = aef_id
                    # doc['apiInvokerId'] = invocationlog.api_invoker_id
                    # doc['apiId'] = invocationlog.logs[i].api_id
                    # doc['apiName'] = invocationlog.logs[i].api_name
                    # doc['apiVersion'] = invocationlog.logs[i].api_version
                    # doc = {
                    #     "logId": secrets.token_hex(15),
                    #     "aefId": aef_id,
                    #     "apiInvokerId": invocationlog.api_invoker_id,
                    #     "apiId": invocationlog.logs[i].api_id,
                    #     "apiName": invocationlog.logs[i].api_name,
                    #     "apiVersion": invocationlog.logs[i].api_version,
                    #     "resourceName": invocationlog.logs[i].resource_name,
                    #     "uri": invocationlog.logs[i].uri,
                    #     "protocol": ,
                    #     "operation": ,
                    #     "result": ,
                    #     "invocationTime": ,
                    #     "invocationLatency": ,
                    #     "inputParameters": ,
                    #     "outputParameters": ,
                    # }

                    self.es.index(index="capiflogs", id=i, document=rec)

                res = Response(json.dumps(invocationlog, cls=JSONEncoder), status=201, mimetype=self.mimetype)

                res.headers['Location'] = "http://localhost:8080/" + str(aef_id) + "/logs/" + str(log_id)
                return res

        except Exception as e:
            exception = "An exception occurred in add services::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)

