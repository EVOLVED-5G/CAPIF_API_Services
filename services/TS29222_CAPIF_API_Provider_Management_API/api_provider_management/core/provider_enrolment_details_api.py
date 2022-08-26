import sys

import pymongo
import secrets
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from bson import json_util
from ..db.db import MongoDatabse

class ProviderManagementOperations:

    def __init__(self):
        self.db = MongoDatabse()

    def register_api_provider_enrolment_details(self, api_provider_enrolment_details):

        try:
            mycol = self.db.get_col_by_name(self.db.provider_enrolment_details)

            # Generate subscriptionID
            apiProvDomId = secrets.token_hex(15)
            registrationId = secrets.token_hex(15)
            provider_enrolment_details = dict()
            provider_enrolment_details["registration_id"] = registrationId
            api_provider_enrolment_details.api_prov_dom_id = apiProvDomId

            provider_enrolment_details.update(api_provider_enrolment_details.to_dict())
            mycol.insert_one(provider_enrolment_details)

            res = Response(json_util.dumps(api_provider_enrolment_details, cls=JSONEncoder),
                        status=201, mimetype='application/json')
            res.headers['Location'] = "http://localhost:8080/api-provider-management/v1/registrations/" + str(registrationId)
            return res

        except Exception as e:
            print("An exception occurred ::", e, file=sys.stderr)
            return False

    def delete_api_provider_enrolment_details(self, registrationId):

        try:
            mycol = self.db.get_col_by_name(self.db.provider_enrolment_details)

            search_filter = {'registration_id': registrationId}
            provider_enrolment_details = mycol.find_one(search_filter)

            if provider_enrolment_details is None:
                prob = ProblemDetails(title="Not Found", status=404, detail="Not Exist Provider Enrolment Details",
                                    cause="Not found registrations to send this api provider details")
                return Response(json.dumps(prob, cls=JSONEncoder), status=404, mimetype='application/json')
            else:
                mycol.delete_one(search_filter)
                return Response(json.dumps(provider_enrolment_details, default=str, cls=JSONEncoder), status=204, mimetype='application/json')

        except Exception as e:
            print("An exception occurred ::", e, file=sys.stderr)
            return False

    def update_api_provider_enrolment_details(self, registrationId, api_provider_enrolment_details):
        try:
            mycol = self.db.get_col_by_name(self.db.provider_enrolment_details)
            search_filter = {'registration_id': registrationId}
            old_provider_enrolment_details = mycol.find_one(search_filter)

            if  old_provider_enrolment_details is None:
                prob = ProblemDetails(title="Not Found", status=404, detail="Not Exist Provider Enrolment Details",
                                    cause="Not found registrations to send this api provider details")
                return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')
            else:
                api_provider_enrolment_details = api_provider_enrolment_details.to_dict()
                api_provider_enrolment_details = {
                    key: value for key, value in api_provider_enrolment_details.items() if value is not None
                }

                mycol.update_one(old_provider_enrolment_details, {"$set":api_provider_enrolment_details}, upsert=False)
                return  Response(json_util.dumps(api_provider_enrolment_details, cls=JSONEncoder), status=200, mimetype='application/json')

        except Exception as e:
            print("An exception occurred ::", e, file=sys.stderr)
            return False

    def patch_api_provider_enrolment_details(self, registrationId, api_provider_enrolment_details_patch):
        try:
            mycol = self.db.get_col_by_name(self.db.provider_enrolment_details)

            search_filter = {'registration_id': registrationId}
            old_provider_enrolment_details = mycol.find_one(search_filter)


            if  old_provider_enrolment_details is None:
                prob = ProblemDetails(title="Not Found", status=404, detail="Not Exist Provider Enrolment Details",
                                    cause="Not found registrations to send this api provider details")
                return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')

            else:

                api_provider_enrolment_details_patch = api_provider_enrolment_details_patch.to_dict()
                api_provider_enrolment_details_patch = {
                    key: value for key, value in api_provider_enrolment_details_patch.items() if value is not None
                }

                mycol.update_one(old_provider_enrolment_details, {"$set":api_provider_enrolment_details_patch})

                return  Response(json_util.dumps(api_provider_enrolment_details_patch, cls=JSONEncoder), status=200, mimetype='application/json')

        except Exception as e:
            print("An exception occurred ::", e, file=sys.stderr)
            return False