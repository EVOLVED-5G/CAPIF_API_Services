import connexion
import six

from flask_jwt_extended import jwt_required, get_jwt_identity
from ..core.provider_enrolment_details_api import ProviderManagementOperations
from api_provider_management.models.api_provider_enrolment_details import APIProviderEnrolmentDetails  # noqa: E501
from api_provider_management.models.problem_details import ProblemDetails  # noqa: E501
from api_provider_management import util


provider_management_ops = ProviderManagementOperations()

def registrations_post(body):  # noqa: E501
    """registrations_post

    Registers a new API Provider domain with API provider domain functions profiles. # noqa: E501

    :param api_provider_enrolment_details: 
    :type api_provider_enrolment_details: dict | bytes

    :rtype: APIProviderEnrolmentDetails
    """


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
    if connexion.request.is_json:
        body = APIProviderEnrolmentDetails.from_dict(connexion.request.get_json())  # noqa: E501
   
    res = provider_management_ops.update_api_provider_enrolment_details(registration_id,body)

    return res
