import connexion
import six

from capif_security.models.access_token_err import AccessTokenErr  # noqa: E501
from capif_security.models.access_token_rsp import AccessTokenRsp  # noqa: E501
from capif_security.models.problem_details import ProblemDetails  # noqa: E501
from capif_security.models.security_notification import SecurityNotification  # noqa: E501
from capif_security.models.service_security import ServiceSecurity  # noqa: E501
from capif_security import util


def securities_security_id_token_post(security_id, grant_type, client_id, client_secret=None, scope=None):  # noqa: E501
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
    return 'do some magic!'


def trusted_invokers_api_invoker_id_delete(api_invoker_id):  # noqa: E501
    """trusted_invokers_api_invoker_id_delete

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str

    :rtype: None
    """
    return 'do some magic!'


def trusted_invokers_api_invoker_id_delete_post(api_invoker_id, security_notification):  # noqa: E501
    """trusted_invokers_api_invoker_id_delete_post

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str
    :param security_notification: Revoke the authorization of the API invoker for APIs.
    :type security_notification: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        security_notification = SecurityNotification.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def trusted_invokers_api_invoker_id_get(api_invoker_id, authentication_info=None, authorization_info=None):  # noqa: E501
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
    return 'do some magic!'


def trusted_invokers_api_invoker_id_put(api_invoker_id, service_security):  # noqa: E501
    """trusted_invokers_api_invoker_id_put

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str
    :param service_security: create a security context for an API invoker
    :type service_security: dict | bytes

    :rtype: ServiceSecurity
    """
    if connexion.request.is_json:
        service_security = ServiceSecurity.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def trusted_invokers_api_invoker_id_update_post(api_invoker_id, service_security):  # noqa: E501
    """trusted_invokers_api_invoker_id_update_post

     # noqa: E501

    :param api_invoker_id: Identifier of an individual API invoker
    :type api_invoker_id: str
    :param service_security: Update the security context (e.g. re-negotiate the security methods).
    :type service_security: dict | bytes

    :rtype: ServiceSecurity
    """
    if connexion.request.is_json:
        service_security = ServiceSecurity.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
