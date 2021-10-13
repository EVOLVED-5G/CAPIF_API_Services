import connexion
import six

from access_control_policy.models.access_control_policy_list import AccessControlPolicyList  # noqa: E501
from access_control_policy.models.problem_details import ProblemDetails  # noqa: E501
from access_control_policy import util


def access_control_policy_list_service_api_id_get(service_api_id, aef_id, api_invoker_id=None, supported_features=None):  # noqa: E501
    """access_control_policy_list_service_api_id_get

    Retrieves the access control policy list. # noqa: E501

    :param service_api_id: Identifier of a published service API
    :type service_api_id: str
    :param aef_id: Identifier of the AEF
    :type aef_id: str
    :param api_invoker_id: Identifier of the API invoker
    :type api_invoker_id: str
    :param supported_features: To filter irrelevant responses related to unsupported features
    :type supported_features: str

    :rtype: AccessControlPolicyList
    """
    return 'do some magic!'
