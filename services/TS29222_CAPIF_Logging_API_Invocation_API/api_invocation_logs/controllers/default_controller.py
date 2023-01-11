import connexion

from api_invocation_logs.models.invocation_log import InvocationLog  # noqa: E501

from ..core.invocationlogs import LoggingInvocationOperations

import json
from flask import Response, request, current_app
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from cryptography import x509
from cryptography.hazmat.backends import default_backend

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
    current_app.logger.info("API Invocation Logs")

    if connexion.request.is_json:
        body = InvocationLog.from_dict(connexion.request.get_json())  # noqa: E501

    res = logging_invocation_operations.add_invocationlog(aef_id, body)

    if res.status_code == 201:
        current_app.logger.info("Invocation Logs stored successfully")

    return res

