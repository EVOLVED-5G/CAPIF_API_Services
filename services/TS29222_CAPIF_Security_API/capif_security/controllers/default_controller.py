import connexion
import six

from capif_security.models.access_token_err import AccessTokenErr  # noqa: E501
from capif_security.models.access_token_rsp import AccessTokenRsp  # noqa: E501
from capif_security.models.access_token_req import AccessTokenReq  # noqa: E501
from capif_security.models.security_notification import SecurityNotification  # noqa: E501
from capif_security.models.service_security import ServiceSecurity  # noqa: E501
from capif_security import util
from ..core import servicesecurity
import json
from flask import Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
import sys


@jwt_required()
def securities_security_id_token_post(security_id, body):  # noqa: E501
    """securities_security_id_token_post

     # noqa: E501

    :param security_id: Identifier of an individual API invoker
    :type security_id: str
    :param grant_type:
    :type grant_type: str
    :param client_id:
    :type client_id: str
    :param client_secret:
    :type client_secret: str
    :param scope:
    :type scope: str

    :rtype: AccessTokenRsp
    """
    identity = get_jwt_identity()
    username, role = identity.split()

    if role != "invoker":
        # prob = ProblemDetails(title="Forbidden", status=403, detail="Role not authorized for this API route",
        #                       cause="User role must be invoker")
        # return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')

        prob = AccessTokenErr(error="invalid_client", error_description="Role not authorized for this API route")
        return Response(json.dumps(prob, cls=JSONEncoder), status=400, mimetype='application/json')

    if connexion.request.is_json:
        body = AccessTokenReq.from_dict(connexion.request.get_json())  # noqa: E501
    res = servicesecurity.return_token(security_id, body)
    return res


@jwt_required()
def trusted_invokers_api_invoker_id_delete(api_invoker_id):  # noqa: E501
    """trusted_invokers_api_invoker_id_delete

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str

    :rtype: None
    """
    identity = get_jwt_identity()
    username, role = identity.split()

    if role != "apf":
        prob = ProblemDetails(title="Forbidden", status=403, detail="Role not authorized for this API route",
                              cause="User role must be apf")
        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')

    return servicesecurity.delete_servicesecurity(api_invoker_id)


@jwt_required()
def trusted_invokers_api_invoker_id_delete_post(api_invoker_id, body):  # noqa: E501
    """trusted_invokers_api_invoker_id_delete_post

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str
    :param security_notification: Revoke the authorization of the API invoker for APIs.
    :type security_notification: dict | bytes

    :rtype: None
    """
    identity = get_jwt_identity()
    username, role = identity.split()

    if role != "apf":
        prob = ProblemDetails(title="Forbidden", status=403, detail="Role not authorized for this API route",
                              cause="User role must be apf")
        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')

    if connexion.request.is_json:
        body = SecurityNotification.from_dict(connexion.request.get_json())  # noqa: E501

    return servicesecurity.revoke_api_authorization(api_invoker_id, body)


@jwt_required()
def trusted_invokers_api_invoker_id_get(api_invoker_id, authentication_info=True, authorization_info=True):  # noqa: E501
    """trusted_invokers_api_invoker_id_get

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str
    :param authentication_info: When set to &#39;true&#39;, it indicates the CAPIF core function to send the authentication information of the API invoker. Set to false or omitted otherwise.
    :type authentication_info: bool
    :param authorization_info: When set to &#39;true&#39;, it indicates the CAPIF core function to send the authorization information of the API invoker. Set to false or omitted otherwise.
    :type authorization_info: bool

    :rtype: ServiceSecurity
    """
    identity = get_jwt_identity()
    username, role = identity.split()

    if role != "apf":
        prob = ProblemDetails(title="Forbidden", status=403, detail="Role not authorized for this API route",
                              cause="User role must be apf")
        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')

    service_security = servicesecurity.get_servicesecurity(api_invoker_id, authentication_info, authorization_info)

    return service_security


@jwt_required()
def trusted_invokers_api_invoker_id_put(api_invoker_id, body):  # noqa: E501
    """trusted_invokers_api_invoker_id_put

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str
    :param service_security: create a security context for an API invoker
    :type service_security: dict | bytes

    :rtype: ServiceSecurity
    """
    identity = get_jwt_identity()
    username, role = identity.split()

    if role != "invoker":
        prob = ProblemDetails(title="Forbidden", status=403, detail="Role not authorized for this API route",
                              cause="User role must be invoker")
        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')

    if connexion.request.is_json:
        body = ServiceSecurity.from_dict(connexion.request.get_json())  # noqa: E501
    res = servicesecurity.create_servicesecurity(api_invoker_id, body)
    return res


@jwt_required()
def trusted_invokers_api_invoker_id_update_post(api_invoker_id, body):  # noqa: E501
    """trusted_invokers_api_invoker_id_update_post

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str
    :param service_security: Update the security context (e.g. re-negotiate the security methods).
    :type service_security: dict | bytes

    :rtype: ServiceSecurity
    """

    identity = get_jwt_identity()
    username, role = identity.split()

    if role != "invoker":
        prob = ProblemDetails(title="Forbidden", status=403, detail="Role not authorized for this API route",
                              cause="User role must be invoker")
        return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')

    if connexion.request.is_json:
        body = ServiceSecurity.from_dict(connexion.request.get_json())  # noqa: E501
    res = servicesecurity.update_servicesecurity(api_invoker_id, body)
    return res
