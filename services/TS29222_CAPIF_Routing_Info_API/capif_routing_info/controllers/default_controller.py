import connexion
import six

from capif_routing_info.models.problem_details import ProblemDetails  # noqa: E501
from capif_routing_info.models.routing_info import RoutingInfo  # noqa: E501
from capif_routing_info import util


def service_apis_service_api_id_get(service_api_id, aef_id, supp_feat=None):  # noqa: E501
    """service_apis_service_api_id_get

    Retrieves the API routing information. # noqa: E501

    :param service_api_id: Identifier of a published service API
    :type service_api_id: str
    :param aef_id: Identifier of the AEF
    :type aef_id: str
    :param supp_feat: To filter irrelevant responses related to unsupported features
    :type supp_feat: str

    :rtype: RoutingInfo
    """
    return 'do some magic!'
