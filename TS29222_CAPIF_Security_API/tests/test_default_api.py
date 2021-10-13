# coding: utf-8

from fastapi.testclient import TestClient


from capif_security.models.access_token_err import AccessTokenErr  # noqa: F401
from capif_security.models.access_token_rsp import AccessTokenRsp  # noqa: F401
from capif_security.models.problem_details import ProblemDetails  # noqa: F401
from capif_security.models.security_notification import SecurityNotification  # noqa: F401
from capif_security.models.service_security import ServiceSecurity  # noqa: F401


def test_securities_security_id_token_post(client: TestClient):
    """Test case for securities_security_id_token_post

    
    """

    headers = {
    }
    data = {
        "grant_type": 'grant_type_example',
        "client_id": 'client_id_example',
        "client_secret": 'client_secret_example',
        "scope": 'scope_example'
    }
    response = client.request(
        "POST",
        "/securities/{securityId}/token".format(securityId='security_id_example'),
        headers=headers,
        data=data,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_trusted_invokers_api_invoker_id_delete(client: TestClient):
    """Test case for trusted_invokers_api_invoker_id_delete

    
    """

    headers = {
    }
    response = client.request(
        "DELETE",
        "/trustedInvokers/{apiInvokerId}".format(apiInvokerId='api_invoker_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_trusted_invokers_api_invoker_id_delete_post(client: TestClient):
    """Test case for trusted_invokers_api_invoker_id_delete_post

    
    """
    security_notification = {"api_invoker_id":"apiInvokerId","aef_id":"aefId","api_ids":["apiIds","apiIds"]}

    headers = {
    }
    response = client.request(
        "POST",
        "/trustedInvokers/{apiInvokerId}/delete".format(apiInvokerId='api_invoker_id_example'),
        headers=headers,
        json=security_notification,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_trusted_invokers_api_invoker_id_get(client: TestClient):
    """Test case for trusted_invokers_api_invoker_id_get

    
    """
    params = [("authentication_info", True),     ("authorization_info", True)]
    headers = {
    }
    response = client.request(
        "GET",
        "/trustedInvokers/{apiInvokerId}".format(apiInvokerId='api_invoker_id_example'),
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_trusted_invokers_api_invoker_id_put(client: TestClient):
    """Test case for trusted_invokers_api_invoker_id_put

    
    """
    service_security = {"notification_destination":"notificationDestination","supported_features":"supportedFeatures","security_info":[{"authentication_info":"authenticationInfo","authorization_info":"authorizationInfo","interface_details":{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":5248,"ipv4_addr":"ipv4Addr"},"pref_security_methods":[None,None],"aef_id":"aefId"},{"authentication_info":"authenticationInfo","authorization_info":"authorizationInfo","interface_details":{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":5248,"ipv4_addr":"ipv4Addr"},"pref_security_methods":[None,None],"aef_id":"aefId"}],"websock_notif_config":{"request_websocket_uri":1,"websocket_uri":"websocketUri"},"request_test_notification":1}

    headers = {
    }
    response = client.request(
        "PUT",
        "/trustedInvokers/{apiInvokerId}".format(apiInvokerId='api_invoker_id_example'),
        headers=headers,
        json=service_security,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_trusted_invokers_api_invoker_id_update_post(client: TestClient):
    """Test case for trusted_invokers_api_invoker_id_update_post

    
    """
    service_security = {"notification_destination":"notificationDestination","supported_features":"supportedFeatures","security_info":[{"authentication_info":"authenticationInfo","authorization_info":"authorizationInfo","interface_details":{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":5248,"ipv4_addr":"ipv4Addr"},"pref_security_methods":[None,None],"aef_id":"aefId"},{"authentication_info":"authenticationInfo","authorization_info":"authorizationInfo","interface_details":{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":5248,"ipv4_addr":"ipv4Addr"},"pref_security_methods":[None,None],"aef_id":"aefId"}],"websock_notif_config":{"request_websocket_uri":1,"websocket_uri":"websocketUri"},"request_test_notification":1}

    headers = {
    }
    response = client.request(
        "POST",
        "/trustedInvokers/{apiInvokerId}/update".format(apiInvokerId='api_invoker_id_example'),
        headers=headers,
        json=service_security,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

