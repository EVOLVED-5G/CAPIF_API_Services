import connexion
import six
import json

from flask import Response, request
from ..core.provider_enrolment_details_api import ProviderManagementOperations
from ..core.check_user import CapifUsersOperations
from ..encoder import JSONEncoder
from api_provider_management.models.api_provider_enrolment_details import APIProviderEnrolmentDetails  # noqa: E501
from api_provider_management.models.problem_details import ProblemDetails  # noqa: E501
from api_provider_management import util
from cryptography.hazmat.backends import default_backend
from flask_jwt_extended import jwt_required, get_jwt_identity
from cryptography import x509
import sys


provider_management_ops = ProviderManagementOperations()
check_user = CapifUsersOperations()

@jwt_required()
def registrations_post(body):  # noqa: E501
    """registrations_post

    Registers a new API Provider domain with API provider domain functions profiles. # noqa: E501

    :param api_provider_enrolment_details: 
    :type api_provider_enrolment_details: dict | bytes

    :rtype: APIProviderEnrolmentDetails
    """

    identity = get_jwt_identity()
    _, role = identity.split()

    if role != "provider":
        prob = ProblemDetails(title="Unauthorized", status=401, detail="Role not authorized for this API route",
                              cause="User role must be provider")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')


    if connexion.request.is_json:
        body = APIProviderEnrolmentDetails.from_dict(connexion.request.get_json())  # noqa: E501


    res = provider_management_ops.register_api_provider_enrolment_details(body)

    return res


def registrations_registration_id_delete(api_prov_dom_id):  # noqa: E501
    """registrations_registration_id_delete

    Deregisters API provider domain by deleting API provider domain and functions. # noqa: E501

    :param registration_id: String identifying an registered API provider domain resource.
    :type registration_id: str

    :rtype: None
    """
    cert_tmp = request.headers['X-Ssl-Client-Cert']
    cert_raw = cert_tmp.replace('\t', '')


    cert = x509.load_pem_x509_certificate(str.encode(cert_raw), default_backend())
    cn = cert.subject.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value.strip()

    capif_user = check_user.check_capif_user(cn, "provider")

    if not capif_user:
        prob = ProblemDetails(title="Unauthorized", status=401, detail="User not authorized",
                              cause="Certificate not authorized")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    res = provider_management_ops.delete_api_provider_enrolment_details(api_prov_dom_id)

    return res


def registrations_registration_id_put(api_prov_dom_id, body):  # noqa: E501
    """registrations_registration_id_put

    Updates an API provider domain&#39;s registration details. # noqa: E501

    :param registration_id: String identifying an registered API provider domain resource.
    :type registration_id: str
    :param api_provider_enrolment_details: Representation of the API provider domain registration details to be updated in CAPIF core function.
    :type api_provider_enrolment_details: dict | bytes

    :rtype: APIProviderEnrolmentDetails
    """
    cert_tmp = request.headers['X-Ssl-Client-Cert']
    cert_raw = cert_tmp.replace('\t', '')


    cert = x509.load_pem_x509_certificate(str.encode(cert_raw), default_backend())
    cn = cert.subject.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value.strip()

    capif_user = check_user.check_capif_user(cn, "provider")

    if not capif_user:
        prob = ProblemDetails(title="Unauthorized", status=401, detail="User not authorized",
                              cause="Certificate not authorized")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = APIProviderEnrolmentDetails.from_dict(connexion.request.get_json())  # noqa: E501

    res = provider_management_ops.update_api_provider_enrolment_details(api_prov_dom_id,body)

    return res
