import connexion
import six

from aef_security.models.check_authentication_req import CheckAuthenticationReq  # noqa: E501
from aef_security.models.check_authentication_rsp import CheckAuthenticationRsp  # noqa: E501
from aef_security.models.problem_details import ProblemDetails  # noqa: E501
from aef_security.models.revoke_authorization_req import RevokeAuthorizationReq  # noqa: E501
from aef_security.models.revoke_authorization_rsp import RevokeAuthorizationRsp  # noqa: E501
from aef_security import util


def check_authentication_post(check_authentication_req):  # noqa: E501
    """Check authentication.

     # noqa: E501

    :param check_authentication_req: 
    :type check_authentication_req: dict | bytes

    :rtype: CheckAuthenticationRsp
    """
    if connexion.request.is_json:
        check_authentication_req = CheckAuthenticationReq.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def revoke_authorization_post(revoke_authorization_req):  # noqa: E501
    """Revoke authorization.

     # noqa: E501

    :param revoke_authorization_req: 
    :type revoke_authorization_req: dict | bytes

    :rtype: RevokeAuthorizationRsp
    """
    if connexion.request.is_json:
        revoke_authorization_req = RevokeAuthorizationReq.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
