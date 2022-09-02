import connexion
import six

from ..core.provider_enrolment_details_api import ProviderManagementOperations
from api_provider_management.models.api_provider_enrolment_details import APIProviderEnrolmentDetails  # noqa: E501
from api_provider_management.models.api_provider_enrolment_details_patch import APIProviderEnrolmentDetailsPatch  # noqa: E501
from api_provider_management.models.problem_details import ProblemDetails  # noqa: E501
from api_provider_management import util

provider_management_ops = ProviderManagementOperations()


def modify_ind_api_provider_enrolment(registration_id, api_provider_enrolment_details_patch):  # noqa: E501
    """modify_ind_api_provider_enrolment

    Modify an individual API provider details. # noqa: E501

    :param registration_id: 
    :type registration_id: str
    :param api_provider_enrolment_details_patch: 
    :type api_provider_enrolment_details_patch: dict | bytes

    :rtype: APIProviderEnrolmentDetails
    """
    if connexion.request.is_json:
        api_provider_enrolment_details_patch = APIProviderEnrolmentDetailsPatch.from_dict(connexion.request.get_json())  # noqa: E501
   
    res = provider_management_ops.patch_api_provider_enrolment_details(registration_id, api_provider_enrolment_details_patch)

    return res
