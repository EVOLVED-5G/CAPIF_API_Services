import connexion

from api_invocation_logs.models.invocation_log import InvocationLog  # noqa: E501

from ..core.check_user import CapifUsersOperations
from ..core.invocationlogs import LoggingInvocationOperations

import json
from flask import Response, request, current_app
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from cryptography import x509
from cryptography.hazmat.backends import default_backend

check_user = CapifUsersOperations()
logging_invocation_operations = LoggingInvocationOperations()


def aef_id_logs_post(aef_id, body):  # noqa: E501
    """aef_id_logs_post

    Creates a new log entry for service API invocations. # noqa: E501

    :param aef_id: Identifier of the API exposing function
    :type aef_id: str
    :param invocation_log: 
    :type invocation_log: dict | bytes

    :rtype: InvocationLog
    """

    cert_tmp = request.headers['X-Ssl-Client-Cert']
    cert_raw = cert_tmp.replace('\t', '')

    cert = x509.load_pem_x509_certificate(str.encode(cert_raw), default_backend())
    cn = cert.subject.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value.strip()

    capif_user = check_user.check_capif_user(cn, "exposer")

    if not capif_user:
        prob = ProblemDetails(title="Unauthorized", status=401, detail="User not authorized",
                              cause="Certificate not authorized")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = InvocationLog.from_dict(connexion.request.get_json())  # noqa: E501

    res = logging_invocation_operations.add_invocationlog(aef_id, body)

    return res

