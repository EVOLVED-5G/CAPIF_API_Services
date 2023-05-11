import connexion
import six
import sys

from logs.models.interface_description import InterfaceDescription  # noqa: E501
from logs.models.invocation_log import InvocationLog  # noqa: E501
from logs.models.operation import Operation  # noqa: E501
from logs.models.problem_details import ProblemDetails  # noqa: E501
from logs.models.protocol import Protocol  # noqa: E501
from logs import util

from ..core.auditoperations import AuditOperations
import json
from flask import Response, request, current_app
from ..encoder import JSONEncoder
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import pymongo
from ..core.responses import bad_request_error

audit_operations = AuditOperations()


def api_invocation_logs_get(aef_id=None, api_invoker_id=None, time_range_start=None, time_range_end=None, api_id=None, api_name=None, api_version=None, protocol=None, operation=None, result=None, resource_name=None, src_interface=None, dest_interface=None, supported_features=None):  # noqa: E501
    """api_invocation_logs_get

    Query and retrieve service API invocation logs stored on the CAPIF core function. # noqa: E501

    :param aef_id: String identifying the API exposing function.
    :type aef_id: str
    :param api_invoker_id: String identifying the API invoker which invoked the service API.
    :type api_invoker_id: str
    :param time_range_start: Start time of the invocation time range.
    :type time_range_start: str
    :param time_range_end: End time of the invocation time range.
    :type time_range_end: str
    :param api_id: String identifying the API invoked.
    :type api_id: str
    :param api_name: API name, it is set as {apiName} part of the URI structure as defined in subclause 4.4 of 3GPP TS 29.501.
    :type api_name: str
    :param api_version: Version of the API which was invoked.
    :type api_version: str
    :param protocol: Protocol invoked.
    :type protocol: dict | bytes
    :param operation: Operation that was invoked on the API.
    :type operation: dict | bytes
    :param result: Result or output of the invocation.
    :type result: str
    :param resource_name: Name of the specific resource invoked.
    :type resource_name: str
    :param src_interface: Interface description of the API invoker.
    :type src_interface: str
    :param dest_interface: Interface description of the API invoked.
    :type dest_interface: str
    :param supported_features: To filter irrelevant responses related to unsupported features
    :type supported_features: str

    :rtype: InvocationLog
    """

    current_app.logger.info("Audit logs")

    if aef_id is None or api_invoker_id is None:
        return bad_request_error(detail="aef_id and api_invoker_id parameters are mandatory",
                                 cause="Mandatory parameters missing", invalid_params=[
                {"param": "aef_id or api_invoker_id", "reason": "missing"}])

    time_range_start = util.deserialize_datetime(time_range_start)
    time_range_end = util.deserialize_datetime(time_range_end)

    query_params = {"aef_id": aef_id,
                    "api_invoker_id": api_invoker_id,
                    "time_range_start": time_range_start,
                    "time_range_end": time_range_end,
                    "api_id": api_id,
                    "api_name": api_name,
                    "api_version": api_version,
                    "protocol": protocol,
                    "operation": operation,
                    "result": result,
                    "resource_name": resource_name,
                    "src_interface": src_interface,
                    "dest_interface": dest_interface,
                    "supported_features": supported_features
                    }

    response = audit_operations.get_logs(query_params)
    return response
