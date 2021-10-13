import connexion
import six

from published_apis.models.problem_details import ProblemDetails  # noqa: E501
from published_apis.models.service_api_description import ServiceAPIDescription  # noqa: E501
from published_apis import util


def apf_id_service_apis_get(apf_id):  # noqa: E501
    """apf_id_service_apis_get

    Retrieve all published APIs. # noqa: E501

    :param apf_id: 
    :type apf_id: str

    :rtype: ServiceAPIDescription
    """
    return 'do some magic!'


def apf_id_service_apis_post(apf_id, service_api_description):  # noqa: E501
    """apf_id_service_apis_post

    Publish a new API. # noqa: E501

    :param apf_id: 
    :type apf_id: str
    :param service_api_description: 
    :type service_api_description: dict | bytes

    :rtype: ServiceAPIDescription
    """
    if connexion.request.is_json:
        service_api_description = ServiceAPIDescription.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def apf_id_service_apis_service_api_id_delete(service_api_id, apf_id):  # noqa: E501
    """apf_id_service_apis_service_api_id_delete

    Unpublish a published service API. # noqa: E501

    :param service_api_id: 
    :type service_api_id: str
    :param apf_id: 
    :type apf_id: str

    :rtype: None
    """
    return 'do some magic!'


def apf_id_service_apis_service_api_id_get(service_api_id, apf_id):  # noqa: E501
    """apf_id_service_apis_service_api_id_get

    Retrieve a published service API. # noqa: E501

    :param service_api_id: 
    :type service_api_id: str
    :param apf_id: 
    :type apf_id: str

    :rtype: ServiceAPIDescription
    """
    return 'do some magic!'


def apf_id_service_apis_service_api_id_put(service_api_id, apf_id, service_api_description):  # noqa: E501
    """apf_id_service_apis_service_api_id_put

    Update a published service API. # noqa: E501

    :param service_api_id: 
    :type service_api_id: str
    :param apf_id: 
    :type apf_id: str
    :param service_api_description: 
    :type service_api_description: dict | bytes

    :rtype: ServiceAPIDescription
    """
    if connexion.request.is_json:
        service_api_description = ServiceAPIDescription.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
