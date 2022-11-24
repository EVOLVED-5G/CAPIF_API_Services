import sys
import os
import pymongo
import secrets
from flask import current_app, Flask, Response
import json

from ..db.db import MongoDatabse
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails


class LoggingInvocationOperations:

    def __init__(self):
        self.db = MongoDatabse()
        self.mimetype = 'application/json'

    def add_invocationlog(self, aef_id, invocationlog):

        mycol = self.db.get_col_by_name(self.db.invocation_logs)
        inv_col = self.db.get_col_by_name(self.db.invoker_details)
        prov_col = self.db.get_col_by_name(self.db.provider_details)
        serv_apis = self.db.get_col_by_name(self.db.service_apis)
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
                for i in range(0, len(invocationlog.logs)):
                    services_api_res = serv_apis.find_one({"$and": [{'api_id': invocationlog.logs[i].api_id}, {'api_name': invocationlog.logs[i].api_name}]})
                    if services_api_res is None:
                        prob = ProblemDetails(title="Service API with id {} and name {} not found".format(invocationlog.logs[i].api_id, invocationlog.logs[i].api_name), status=404, detail="Please provide an existing Service API id or name", cause="Not existing API ID")
                        return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype=self.mimetype)

                log_id = secrets.token_hex(15)
                rec = dict()
                rec['log_id'] = log_id
                rec.update(invocationlog.to_dict())
                mycol.insert_one(rec)
                res = Response(json.dumps(invocationlog, cls=JSONEncoder), status=201, mimetype=self.mimetype)
                res.headers['Location'] = "https://{}/api-invocation-logs/v1/{}/logs/{}".format(os.getenv('CAPIF_HOSTNAME'), str(aef_id), str(log_id))
                return res

        except Exception as e:
            exception = "An exception occurred in add services::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)

