# coding: utf-8

from fastapi.testclient import TestClient


from api_invocation_logs.models.invocation_log import InvocationLog  # noqa: F401
from api_invocation_logs.models.problem_details import ProblemDetails  # noqa: F401


def test_aef_id_logs_post(client: TestClient):
    """Test case for aef_id_logs_post

    
    """
    invocation_log = {"supported_features":"supportedFeatures","api_invoker_id":"apiInvokerId","aef_id":"aefId","logs":[{"api_name":"apiName","invocation_time":"2000-01-23T04:56:07.000+00:00","src_interface":{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":39500,"ipv4_addr":"ipv4Addr"},"fwd_interface":"fwdInterface","resource_name":"resourceName","uri":"uri","input_parameters":"","invocation_latency":0,"result":"result","api_version":"apiVersion","dest_interface":{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":39500,"ipv4_addr":"ipv4Addr"},"api_id":"apiId","output_parameters":""},{"api_name":"apiName","invocation_time":"2000-01-23T04:56:07.000+00:00","src_interface":{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":39500,"ipv4_addr":"ipv4Addr"},"fwd_interface":"fwdInterface","resource_name":"resourceName","uri":"uri","input_parameters":"","invocation_latency":0,"result":"result","api_version":"apiVersion","dest_interface":{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":39500,"ipv4_addr":"ipv4Addr"},"api_id":"apiId","output_parameters":""}]}

    headers = {
    }
    response = client.request(
        "POST",
        "/{aefId}/logs".format(aefId='aef_id_example'),
        headers=headers,
        json=invocation_log,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

