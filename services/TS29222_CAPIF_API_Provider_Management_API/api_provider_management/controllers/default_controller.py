import connexion
import six
import json

from flask import Response, request, current_app
from ..core.provider_enrolment_details_api import ProviderManagementOperations
from ..encoder import JSONEncoder
from api_provider_management.models.api_provider_enrolment_details import APIProviderEnrolmentDetails  # noqa: E501
from api_provider_management.models.problem_details import ProblemDetails  # noqa: E501
from api_provider_management import util
from cryptography.hazmat.backends import default_backend
from flask_jwt_extended import jwt_required, get_jwt_identity
from cryptography import x509
import sys


provider_management_ops = ProviderManagementOperations()

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

    current_app.logger.info("Registering Provider Domain")
    if role != "provider":
        prob = ProblemDetails(title="Unauthorized", status=401, detail="Role not authorized for this API route",
                              cause="User role must be provider")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')


    if connexion.request.is_json:
        body = APIProviderEnrolmentDetails.from_dict(connexion.request.get_json())  # noqa: E501


    res = provider_management_ops.register_api_provider_enrolment_details(body)

    return res


def registrations_registration_id_delete(registration_id):  # noqa: E501
    """registrations_registration_id_delete

    Deregisters API provider domain by deleting API provider domain and functions. # noqa: E501

    :param registration_id: String identifying an registered API provider domain resource.
    :type registration_id: str

    :rtype: None
    """
    current_app.logger.info("Removing Provider Domain")
    res = provider_management_ops.delete_api_provider_enrolment_details(registration_id)

    return res


def registrations_registration_id_put(registration_id, body):  # noqa: E501
    """registrations_registration_id_put

    Updates an API provider domain&#39;s registration details. # noqa: E501

    :param registration_id: String identifying an registered API provider domain resource.
    :type registration_id: str
    :param api_provider_enrolment_details: Representation of the API provider domain registration details to be updated in CAPIF core function.
    :type api_provider_enrolment_details: dict | bytes

    :rtype: APIProviderEnrolmentDetails
    """
    current_app.logger.info("Updating Provider Domain")
    if connexion.request.is_json:
        body = APIProviderEnrolmentDetails.from_dict(connexion.request.get_json())  # noqa: E501

    res = provider_management_ops.update_api_provider_enrolment_details(registration_id,body)

    return res
