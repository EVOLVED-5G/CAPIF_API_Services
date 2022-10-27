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


class LoggingInvocationOperations:

    def __init__(self):
        self.db = MongoDatabse()
        self.mimetype = 'application/json'

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
                del invocationlog_copy['logs']
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

                res = Response(json.dumps(invocationlog, cls=JSONEncoder), status=201, mimetype=self.mimetype)

                res.headers['Location'] = "http://localhost:8080/" + str(aef_id) + "/logs/" + str(log_id)
                return res

        except Exception as e:
            exception = "An exception occurred in add services::", e
            return Response(json.dumps(exception, default=str, cls=JSONEncoder), status=500, mimetype=self.mimetype)

