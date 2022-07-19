import connexion
from published_apis.models.service_api_description import ServiceAPIDescription  # noqa: E501
from ..core import serviceapidescriptions

import json
from flask import Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails

mqtt = current_app.config['INSTANCE_MQTT']

@jwt_required()
def apf_id_service_apis_get(apf_id):  # noqa: E501
    """apf_id_service_apis_get

    Retrieve all published APIs. # noqa: E501

    :param apf_id: 
    :type apf_id: str

    :rtype: ServiceAPIDescription
    """

    identity = get_jwt_identity()
    _, role = identity.split()

    if role != "apf":
        prob = ProblemDetails(title="Unauthorized", status=401, detail="Role not authorized for this API route",
                              cause="User role must be apf")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    # service_apis = serviceapidescriptions.get_serviceapis(apf_id)
    # response = service_apis, 200

    res = serviceapidescriptions.get_serviceapis(apf_id)

    return res


@jwt_required()
def apf_id_service_apis_post(apf_id, body):  # noqa: E501
    """apf_id_service_apis_post

    Publish a new API. # noqa: E501

    :param apf_id: 
    :type apf_id: str
    :param service_api_description: 
    :type service_api_description: dict | bytes

    :rtype: ServiceAPIDescription
    """
    identity = get_jwt_identity()
    _, role = identity.split()

    if role != "apf":
        prob = ProblemDetails(title="Unauthorized", status=401, detail="Role not authorized for this API route",
                              cause="User role must be apf")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = ServiceAPIDescription.from_dict(connexion.request.get_json())  # noqa: E501

    res = serviceapidescriptions.add_serviceapidescription(apf_id, body)
   
    if res.status_code == 201:
        mqtt.publish("/events","SERVICE_API_AVAILABLE")
    return res


@jwt_required()
def apf_id_service_apis_service_api_id_delete(service_api_id, apf_id):  # noqa: E501
    """apf_id_service_apis_service_api_id_delete

    Unpublish a published service API. # noqa: E501

    :param service_api_id: 
    :type service_api_id: str
    :param apf_id: 
    :type apf_id: str

    :rtype: None
    """

    identity = get_jwt_identity()
    _, role = identity.split()

    if role != "apf":
        prob = ProblemDetails(title="Unauthorized", status=401, detail="Role not authorized for this API route",
                              cause="User role must be apf")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = ServiceAPIDescription.from_dict(connexion.request.get_json())  # noqa: E501

    # service_apis = serviceapidescriptions.delete_serviceapidescription(service_api_id, apf_id)
    # response = service_apis, 204

    res = serviceapidescriptions.delete_serviceapidescription(service_api_id, apf_id)

    if res.status_code == 204:
        mqtt.publish("/events","SERVICE_API_UNAVAILABLE")
    return res


@jwt_required()
def apf_id_service_apis_service_api_id_get(service_api_id, apf_id):  # noqa: E501
    """apf_id_service_apis_service_api_id_get

    Retrieve a published service API. # noqa: E501

    :param service_api_id: 
    :type service_api_id: str
    :param apf_id: 
    :type apf_id: str

    :rtype: ServiceAPIDescription
    """
    identity = get_jwt_identity()
    _, role = identity.split()

    if role != "apf":
        prob = ProblemDetails(title="Unauthorized", status=401, detail="Role not authorized for this API route",
                              cause="User role must be apf")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    # service_apis = serviceapidescriptions.get_one_serviceapi(service_api_id, apf_id)
    # response = service_apis, 200

    res = serviceapidescriptions.get_one_serviceapi(service_api_id, apf_id)

    return res


@jwt_required()
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
    identity = get_jwt_identity()
    _, role = identity.split()

    if role != "apf":
        prob = ProblemDetails(title="Unauthorized", status=401, detail="Role not authorized for this API route",
                              cause="User role must be apf")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = ServiceAPIDescription.from_dict(connexion.request.get_json())  # noqa: E501

    response = serviceapidescriptions.update_serviceapidescription(service_api_id, apf_id, body)

    if response.status_code == 200:
        mqtt.publish("/events","SERVICE_API_UPDATE")
    # return response,200
    return response
