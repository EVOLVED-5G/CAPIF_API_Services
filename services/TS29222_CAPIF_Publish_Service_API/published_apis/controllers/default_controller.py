import connexion
from published_apis.models.service_api_description import ServiceAPIDescription  # noqa: E501
from ..core import serviceapidescriptions
from ..core.serviceapidescriptions import PublishServiceOperations
from ..core.publisher import Publisher

import json
from flask import Response, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import pymongo


service_operations = PublishServiceOperations()
publisher_ops = Publisher()

def apf_id_service_apis_get(apf_id):  # noqa: E501
    """apf_id_service_apis_get

    Retrieve all published APIs. # noqa: E501

    :param apf_id: 
    :type apf_id: str

    :rtype: ServiceAPIDescription
    """
    current_app.logger.info("Obtainig all service published")
    res = service_operations.get_serviceapis(apf_id)

    return res


def apf_id_service_apis_post(apf_id, body):  # noqa: E501
    """apf_id_service_apis_post

    Publish a new API. # noqa: E501

    :param apf_id: 
    :type apf_id: str
    :param service_api_description: 
    :type service_api_description: dict | bytes

    :rtype: ServiceAPIDescription
    """

    current_app.logger.info("Publishing service")
    if connexion.request.is_json:
        body = ServiceAPIDescription.from_dict(connexion.request.get_json())  # noqa: E501

    res = service_operations.add_serviceapidescription(apf_id, body)

    if res.status_code == 201:
        current_app.logger.info("Service published")
        publisher_ops.publish_message("events", "SERVICE_API_AVAILABLE")

    return res


def apf_id_service_apis_service_api_id_delete(service_api_id, apf_id):  # noqa: E501
    """apf_id_service_apis_service_api_id_delete

    Unpublish a published service API. # noqa: E501

    :param service_api_id: 
    :type service_api_id: str
    :param apf_id: 
    :type apf_id: str

    :rtype: None
    """

    current_app.logger.info("Removing service published")
    res = service_operations.delete_serviceapidescription(service_api_id, apf_id)

    if res.status_code == 204:
        current_app.logger.info("Removed service published")
        publisher_ops.publish_message("events", "SERVICE_API_UNAVAILABLE")
        publisher_ops.publish_message("internal-messages", f"service-removed:{service_api_id}")

    return res


def apf_id_service_apis_service_api_id_get(service_api_id, apf_id):  # noqa: E501
    """apf_id_service_apis_service_api_id_get

    Retrieve a published service API. # noqa: E501

    :param service_api_id: 
    :type service_api_id: str
    :param apf_id: 
    :type apf_id: str

    :rtype: ServiceAPIDescription
    """

    current_app.logger.info("Obtaining service api with id: " + service_api_id)
    res = service_operations.get_one_serviceapi(service_api_id, apf_id)

    return res


def apf_id_service_apis_service_api_id_put(service_api_id, apf_id, body):  # noqa: E501
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

    current_app.logger.info("Updating service api id with id: " + service_api_id)

    if connexion.request.is_json:
        body = ServiceAPIDescription.from_dict(connexion.request.get_json())  # noqa: E501

    response = service_operations.update_serviceapidescription(service_api_id, apf_id, body)

    if response.status_code == 200:
        publisher_ops.publish_message("events", "SERVICE_API_UPDATE")

    return response
