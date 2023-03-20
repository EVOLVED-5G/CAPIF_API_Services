import connexion
import six

from capif_security.models.access_token_err import AccessTokenErr  # noqa: E501
from capif_security.models.access_token_rsp import AccessTokenRsp  # noqa: E501
from capif_security.models.access_token_req import AccessTokenReq  # noqa: E501
from capif_security.models.security_notification import SecurityNotification  # noqa: E501
from capif_security.models.service_security import ServiceSecurity  # noqa: E501
from capif_security import util
from ..core.servicesecurity import SecurityOperations
from ..core.consumer_messager import Subscriber
from ..core.publisher import Publisher
import json
from flask import Response, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from ..core.validate_user import ControlAccess
from functools import wraps
import pymongo

service_security_ops = SecurityOperations()
publish_ops = Publisher()

valid_user = ControlAccess()

def cert_validation():
    def _cert_validation(f):
        @wraps(f)
        def __cert_validation(*args, **kwargs):
            #just do here everything what you need

            args = request.view_args
            cert_tmp = request.headers['X-Ssl-Client-Cert']
            cert_raw = cert_tmp.replace('\t', '')

            cert = x509.load_pem_x509_certificate(str.encode(cert_raw), default_backend())

            cn = cert.subject.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value.strip()

            if cn != "superadmin" and cn != "aef":
                cert_signature = cert.signature.hex()

                if "securityId" in args:
                    result = valid_user.validate_user_cert(args["securityId"], cert_signature)
                else:
                    result = valid_user.validate_user_cert(args["apiInvokerId"], cert_signature)

                if result is not None:
                    return result

            result = f(**kwargs)
            return result
        return __cert_validation
    return _cert_validation

@cert_validation()
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

    current_app.logger.info("Creating security token")
    if connexion.request.is_json:
        body = AccessTokenReq.from_dict(connexion.request.get_json())  # noqa: E501
    res = service_security_ops.return_token(security_id, body)


    return res

@cert_validation()
def trusted_invokers_api_invoker_id_delete(api_invoker_id):  # noqa: E501
    """trusted_invokers_api_invoker_id_delete

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str

    :rtype: None
    """
    current_app.logger.info("Removing security context")
    return service_security_ops.delete_servicesecurity(api_invoker_id)

@cert_validation()
def trusted_invokers_api_invoker_id_delete_post(api_invoker_id, body):  # noqa: E501
    """trusted_invokers_api_invoker_id_delete_post

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str
    :param security_notification: Revoke the authorization of the API invoker for APIs.
    :type security_notification: dict | bytes

    :rtype: None
    """

    if connexion.request.is_json:
        body = SecurityNotification.from_dict(connexion.request.get_json())  # noqa: E501

    current_app.logger.info("Revoking permissions")
    res = service_security_ops.revoke_api_authorization(api_invoker_id, body)
    if res.status_code == 204:
        current_app.logger.info("Permissions revoked")
        publish_ops.publish_message("events", "API_INVOKER_AUTHORIZATION_REVOKED")

    return res

@cert_validation()
def trusted_invokers_api_invoker_id_get(api_invoker_id, authentication_info=False, authorization_info=False):  # noqa: E501
    """trusted_invokers_api_invoker_id_get

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str
    :param authentication_info: When set to &#39;true&#39;, it indicates the CAPIF core function to send the authentication information of the API invoker. Set to false or omitted otherwise.
    :type authentication_info: bool
    :param authorization_info: When set to &#39;true&#39;, it indicates the CAPIF core function to send the authorization information of the API invoker. Set to false or omitted otherwise.
    :type authorization_info: bool

    :rtype: Union[ServiceSecurity, Tuple[ServiceSecurity, int], Tuple[ServiceSecurity, int, Dict[str, str]]
    """

    current_app.logger.info("Obtaining security context")
    res = service_security_ops.get_servicesecurity(api_invoker_id, authentication_info, authorization_info)

    return res

@cert_validation()
def trusted_invokers_api_invoker_id_put(api_invoker_id, body):  # noqa: E501
    """trusted_invokers_api_invoker_id_put

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str
    :param service_security: create a security context for an API invoker
    :type service_security: dict | bytes

    :rtype: Union[ServiceSecurity, Tuple[ServiceSecurity, int], Tuple[ServiceSecurity, int, Dict[str, str]]
    """
    current_app.logger.info("Creating security context")

    if connexion.request.is_json:
        body = ServiceSecurity.from_dict(connexion.request.get_json())  # noqa: E501
    res = service_security_ops.create_servicesecurity(api_invoker_id, body)

    if res.status_code == 201:
        for service_instance in body.security_info:
            if service_instance.api_id is not None:
                publish_ops.publish_message("internal-messages", "security-context-created:"+api_invoker_id+":"+service_instance.api_id )

    return res

@cert_validation()
def trusted_invokers_api_invoker_id_update_post(api_invoker_id, body):  # noqa: E501
    """trusted_invokers_api_invoker_id_update_post

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str
    :param service_security: Update the security context (e.g. re-negotiate the security methods).
    :type service_security: dict | bytes

    :rtype: ServiceSecurity
    """
    current_app.logger.info("Updating security context")

    if connexion.request.is_json:
        body = ServiceSecurity.from_dict(connexion.request.get_json())  # noqa: E501
    res = service_security_ops.update_servicesecurity(api_invoker_id, body)
    return res
