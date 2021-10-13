import connexion
import six

from api_provider_management.models.api_provider_enrolment_details import APIProviderEnrolmentDetails  # noqa: E501
from api_provider_management.models.problem_details import ProblemDetails  # noqa: E501
from api_provider_management import util


def registrations_post(api_provider_enrolment_details):  # noqa: E501
    """registrations_post

    Registers a new API Provider domain with API provider domain functions profiles. # noqa: E501

    :param api_provider_enrolment_details: 
    :type api_provider_enrolment_details: dict | bytes

    :rtype: APIProviderEnrolmentDetails
    """
    if connexion.request.is_json:
        api_provider_enrolment_details = APIProviderEnrolmentDetails.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def registrations_registration_id_delete(registration_id):  # noqa: E501
    """registrations_registration_id_delete

    Deregisters API provider domain by deleting API provider domain and functions. # noqa: E501

    :param registration_id: String identifying an registered API provider domain resource.
    :type registration_id: str

    :rtype: None
    """
    return 'do some magic!'


def registrations_registration_id_put(registration_id, api_provider_enrolment_details):  # noqa: E501
    """registrations_registration_id_put

    Updates an API provider domain&#39;s registration details. # noqa: E501

    :param registration_id: String identifying an registered API provider domain resource.
    :type registration_id: str
    :param api_provider_enrolment_details: Representation of the API provider domain registration details to be updated in CAPIF core function.
    :type api_provider_enrolment_details: dict | bytes

    :rtype: APIProviderEnrolmentDetails
    """
    if connexion.request.is_json:
        api_provider_enrolment_details = APIProviderEnrolmentDetails.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
