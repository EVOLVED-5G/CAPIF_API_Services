from email.quoprimime import body_decode
import connexion
import six
import json

from flask import Response, request, current_app
from ..core.provider_enrolment_details_api import ProviderManagementOperations
from ..encoder import JSONEncoder
from api_provider_management.models.api_provider_enrolment_details import APIProviderEnrolmentDetails  # noqa: E501
from api_provider_management.models.api_provider_enrolment_details_patch import APIProviderEnrolmentDetailsPatch  # noqa: E501
from api_provider_management.models.problem_details import ProblemDetails  # noqa: E501
from api_provider_management import util
from cryptography.hazmat.backends import default_backend
from cryptography import x509

provider_management_ops = ProviderManagementOperations()


def modify_ind_api_provider_enrolment(registration_id, body):  # noqa: E501
    """modify_ind_api_provider_enrolment

    Modify an individual API provider details. # noqa: E501

    :param registration_id: 
    :type registration_id: str
    :param api_provider_enrolment_details_patch: 
    :type api_provider_enrolment_details_patch: dict | bytes

    :rtype: APIProviderEnrolmentDetails
    """

    current_app.logger.info("Patch Provider Domain")
    if connexion.request.is_json:
        body = APIProviderEnrolmentDetailsPatch.from_dict(connexion.request.get_json())  # noqa: E501

    res = provider_management_ops.patch_api_provider_enrolment_details(registration_id, body)

    return res
