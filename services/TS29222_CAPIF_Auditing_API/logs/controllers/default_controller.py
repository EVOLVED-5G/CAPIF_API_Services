import connexion
import six
import sys

from logs.models.interface_description import InterfaceDescription  # noqa: E501
from logs.models.invocation_log import InvocationLog  # noqa: E501
from logs.models.operation import Operation  # noqa: E501
from logs.models.problem_details import ProblemDetails  # noqa: E501
from logs.models.protocol import Protocol  # noqa: E501
from logs import util

from ..core.check_user import CapifUsersOperations
from ..core.auditoperations import AuditOperations
import json
from flask import Response, request, current_app
from ..encoder import JSONEncoder
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import pymongo


check_user = CapifUsersOperations()
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

    time_range_start = util.deserialize_datetime(time_range_start)
    time_range_end = util.deserialize_datetime(time_range_end)

    # if connexion.request.is_json:
    #     protocol = Protocol.from_dict(connexion.request.get_json())  # noqa: E501
    # if connexion.request.is_json:
    #     operation = Operation.from_dict(connexion.request.get_json())  # noqa: E501
    # if connexion.request.is_json:
    #     src_interface = InterfaceDescription.from_dict(connexion.request.get_json())  # noqa: E501
    # if connexion.request.is_json:
    #     dest_interface = InterfaceDescription.from_dict(connexion.request.get_json())  # noqa: E501

    # cert_tmp = request.headers['X-Ssl-Client-Cert']
    # cert_raw = cert_tmp.replace('\t', '')
    #
    # cert = x509.load_pem_x509_certificate(str.encode(cert_raw), default_backend())
    # cn = cert.subject.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value.strip()
    #
    # capif_user = check_user.check_capif_user(cn, "invoker")
    #
    # if not capif_user:
    #     prob = ProblemDetails(title="Unauthorized", status=401, detail="User not authorized",
    #                           cause="Certificate not authorized")
    #     return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')
    #
    # else:
    #     response = discover_apis.get_discoveredapis(api_invoker_id, api_name, api_version, comm_type, protocol, aef_id, data_format, api_cat, supported_features, api_supported_features)
    #     return response

    response = audit_operations.get_logs(aef_id, api_invoker_id, time_range_start, time_range_end, api_id, api_name, api_version, protocol, operation, result, resource_name, src_interface, dest_interface, supported_features)
    return response
