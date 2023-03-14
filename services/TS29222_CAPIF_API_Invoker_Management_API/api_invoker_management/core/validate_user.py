from flask import current_app, Response
import json
from ..models.problem_details import ProblemDetails
from ..encoder import JSONEncoder
from .resources import Resource

class ControlAccess(Resource):

    def validate_user_cert(self, api_invoker_id, cert_signature):

        cert_col = self.db.get_col_by_name(self.db.certs_col)

        try:
            my_query = {'id':api_invoker_id}
            cert_entry = cert_col.find_one(my_query)

            if cert_entry is not None:
                if cert_entry["cert"] != cert_signature:
                    prob = ProblemDetails(title="Unauthorized", detail="User not authorized", cause="You are not the owner of this resource")
                    return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype="application/json")

        except Exception as e:
            exception = "An exception occurred in validate invoker"
            current_app.logger.error(exception + "::" + str(e))
            return internal_server_error(detail=exception, cause=str(e))