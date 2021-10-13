# coding: utf-8

from fastapi.testclient import TestClient


from capif_routing_info.models.problem_details import ProblemDetails  # noqa: F401
from capif_routing_info.models.routing_info import RoutingInfo  # noqa: F401


def test_service_apis_service_api_id_get(client: TestClient):
    """Test case for service_apis_service_api_id_get

    
    """
    params = [("aef_id", 'aef_id_example'),     ("supp_feat", 'supp_feat_example')]
    headers = {
    }
    response = client.request(
        "GET",
        "/service-apis/{serviceApiId}".format(serviceApiId='service_api_id_example'),
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

