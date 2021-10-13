# coding: utf-8

from fastapi.testclient import TestClient


from access_control_policy.models.access_control_policy_list import AccessControlPolicyList  # noqa: F401
from access_control_policy.models.problem_details import ProblemDetails  # noqa: F401


def test_access_control_policy_list_service_api_id_get(client: TestClient):
    """Test case for access_control_policy_list_service_api_id_get

    
    """
    params = [("aef_id", 'aef_id_example'),     ("api_invoker_id", 'api_invoker_id_example'),     ("supported_features", 'supported_features_example')]
    headers = {
    }
    response = client.request(
        "GET",
        "/accessControlPolicyList/{serviceApiId}".format(serviceApiId='service_api_id_example'),
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

