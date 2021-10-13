# coding: utf-8

from fastapi.testclient import TestClient


from aef_security.models.check_authentication_req import CheckAuthenticationReq  # noqa: F401
from aef_security.models.check_authentication_rsp import CheckAuthenticationRsp  # noqa: F401
from aef_security.models.problem_details import ProblemDetails  # noqa: F401
from aef_security.models.revoke_authorization_req import RevokeAuthorizationReq  # noqa: F401
from aef_security.models.revoke_authorization_rsp import RevokeAuthorizationRsp  # noqa: F401


def test_check_authentication_post(client: TestClient):
    """Test case for check_authentication_post

    Check authentication.
    """
    check_authentication_req = {"supported_features":"supportedFeatures","api_invoker_id":"apiInvokerId"}

    headers = {
    }
    response = client.request(
        "POST",
        "/check-authentication",
        headers=headers,
        json=check_authentication_req,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_revoke_authorization_post(client: TestClient):
    """Test case for revoke_authorization_post

    Revoke authorization.
    """
    revoke_authorization_req = {"supported_features":"supportedFeatures","revoke_info":{"api_invoker_id":"apiInvokerId","aef_id":"aefId","api_ids":["apiIds","apiIds"]}}

    headers = {
    }
    response = client.request(
        "POST",
        "/revoke-authorization",
        headers=headers,
        json=revoke_authorization_req,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

