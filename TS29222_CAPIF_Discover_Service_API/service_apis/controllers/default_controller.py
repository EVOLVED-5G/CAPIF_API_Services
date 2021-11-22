from ..core import discoveredapis
import json
from flask import Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails


@jwt_required()
def all_service_apis_get(api_invoker_id, api_name=None, api_version=None, comm_type=None, protocol=None, aef_id=None, data_format=None, api_cat=None, supported_features=None, api_supported_features=None):  # noqa: E501
    """all_service_apis_get

    Discover published service APIs and retrieve a collection of APIs according to certain filter criteria. # noqa: E501

    :param api_invoker_id: String identifying the API invoker assigned by the CAPIF core function. It also represents the CCF identifier in the CAPIF-6/6e interface.
    :type api_invoker_id: str
    :param api_name: API name, it is set as {apiName} part of the URI structure as defined in subclause 4.4 of 3GPP TS 29.501.
    :type api_name: str
    :param api_version: API major version the URI (e.g. v1).
    :type api_version: str
    :param comm_type: Communication type used by the API (e.g. REQUEST_RESPONSE).
    :type comm_type: dict | bytes
    :param protocol: Protocol used by the API.
    :type protocol: dict | bytes
    :param aef_id: AEF identifer.
    :type aef_id: str
    :param data_format: Data formats used by the API (e.g. serialization protocol JSON used).
    :type data_format: dict | bytes
    :param api_cat: The service API category to which the service API belongs to.
    :type api_cat: str
    :param supported_features: Features supported by the NF consumer for the CAPIF Discover Service API.
    :type supported_features: str
    :param api_supported_features: Features supported by the discovered service API indicated by api-name parameter. This may only be present if api-name query parameter is present.
    :type api_supported_features: str

    :rtype: DiscoveredAPIs
    """

    identity = get_jwt_identity()
    username, role = identity.split()

    if role != "invoker":
        prob = ProblemDetails(title="Unauthorized", status=401, detail="Role not authorized for this API route",
                              cause="User role must be invoker")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    discovered_apis = discoveredapis.get_discoveredapis(api_invoker_id, api_name, api_version, comm_type, protocol, aef_id, data_format, api_cat, supported_features, api_supported_features)
    response = discovered_apis, 200

    return response
