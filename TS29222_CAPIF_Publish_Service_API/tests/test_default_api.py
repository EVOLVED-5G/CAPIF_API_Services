# coding: utf-8

from fastapi.testclient import TestClient


from published_apis.models.problem_details import ProblemDetails  # noqa: F401
from published_apis.models.service_api_description import ServiceAPIDescription  # noqa: F401


def test_apf_id_service_apis_get(client: TestClient):
    """Test case for apf_id_service_apis_get

    
    """

    headers = {
    }
    response = client.request(
        "GET",
        "/{apfId}/service-apis".format(apfId='apf_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_apf_id_service_apis_post(client: TestClient):
    """Test case for apf_id_service_apis_post

    
    """
    service_api_description = {"service_api_category":"serviceAPICategory","ccf_id":"ccfId","api_name":"apiName","shareable_info":{"capif_prov_doms":["capifProvDoms","capifProvDoms"],"is_shareable":1},"supported_features":"supportedFeatures","description":"description","api_supp_feats":"apiSuppFeats","api_id":"apiId","aef_profiles":[{"security_methods":[None,None],"versions":[{"api_version":"apiVersion","resources":[{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"},{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"}],"cust_operations":[{"operations":[None,None],"description":"description","cust_op_name":"custOpName"},{"operations":[None,None],"description":"description","cust_op_name":"custOpName"}],"expiry":"2000-01-23T04:56:07.000+00:00"},{"api_version":"apiVersion","resources":[{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"},{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"}],"cust_operations":[{"operations":[None,None],"description":"description","cust_op_name":"custOpName"},{"operations":[None,None],"description":"description","cust_op_name":"custOpName"}],"expiry":"2000-01-23T04:56:07.000+00:00"}],"domain_name":"domainName","aef_id":"aefId","interface_descriptions":[{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":5248,"ipv4_addr":"ipv4Addr"},{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":5248,"ipv4_addr":"ipv4Addr"}]},{"security_methods":[None,None],"versions":[{"api_version":"apiVersion","resources":[{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"},{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"}],"cust_operations":[{"operations":[None,None],"description":"description","cust_op_name":"custOpName"},{"operations":[None,None],"description":"description","cust_op_name":"custOpName"}],"expiry":"2000-01-23T04:56:07.000+00:00"},{"api_version":"apiVersion","resources":[{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"},{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"}],"cust_operations":[{"operations":[None,None],"description":"description","cust_op_name":"custOpName"},{"operations":[None,None],"description":"description","cust_op_name":"custOpName"}],"expiry":"2000-01-23T04:56:07.000+00:00"}],"domain_name":"domainName","aef_id":"aefId","interface_descriptions":[{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":5248,"ipv4_addr":"ipv4Addr"},{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":5248,"ipv4_addr":"ipv4Addr"}]}],"pub_api_path":{"ccf_ids":["ccfIds","ccfIds"]}}

    headers = {
    }
    response = client.request(
        "POST",
        "/{apfId}/service-apis".format(apfId='apf_id_example'),
        headers=headers,
        json=service_api_description,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_apf_id_service_apis_service_api_id_delete(client: TestClient):
    """Test case for apf_id_service_apis_service_api_id_delete

    
    """

    headers = {
    }
    response = client.request(
        "DELETE",
        "/{apfId}/service-apis/{serviceApiId}".format(serviceApiId='service_api_id_example', apfId='apf_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_apf_id_service_apis_service_api_id_get(client: TestClient):
    """Test case for apf_id_service_apis_service_api_id_get

    
    """

    headers = {
    }
    response = client.request(
        "GET",
        "/{apfId}/service-apis/{serviceApiId}".format(serviceApiId='service_api_id_example', apfId='apf_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_apf_id_service_apis_service_api_id_put(client: TestClient):
    """Test case for apf_id_service_apis_service_api_id_put

    
    """
    service_api_description = {"service_api_category":"serviceAPICategory","ccf_id":"ccfId","api_name":"apiName","shareable_info":{"capif_prov_doms":["capifProvDoms","capifProvDoms"],"is_shareable":1},"supported_features":"supportedFeatures","description":"description","api_supp_feats":"apiSuppFeats","api_id":"apiId","aef_profiles":[{"security_methods":[None,None],"versions":[{"api_version":"apiVersion","resources":[{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"},{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"}],"cust_operations":[{"operations":[None,None],"description":"description","cust_op_name":"custOpName"},{"operations":[None,None],"description":"description","cust_op_name":"custOpName"}],"expiry":"2000-01-23T04:56:07.000+00:00"},{"api_version":"apiVersion","resources":[{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"},{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"}],"cust_operations":[{"operations":[None,None],"description":"description","cust_op_name":"custOpName"},{"operations":[None,None],"description":"description","cust_op_name":"custOpName"}],"expiry":"2000-01-23T04:56:07.000+00:00"}],"domain_name":"domainName","aef_id":"aefId","interface_descriptions":[{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":5248,"ipv4_addr":"ipv4Addr"},{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":5248,"ipv4_addr":"ipv4Addr"}]},{"security_methods":[None,None],"versions":[{"api_version":"apiVersion","resources":[{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"},{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"}],"cust_operations":[{"operations":[None,None],"description":"description","cust_op_name":"custOpName"},{"operations":[None,None],"description":"description","cust_op_name":"custOpName"}],"expiry":"2000-01-23T04:56:07.000+00:00"},{"api_version":"apiVersion","resources":[{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"},{"operations":[None,None],"description":"description","resource_name":"resourceName","cust_op_name":"custOpName","uri":"uri"}],"cust_operations":[{"operations":[None,None],"description":"description","cust_op_name":"custOpName"},{"operations":[None,None],"description":"description","cust_op_name":"custOpName"}],"expiry":"2000-01-23T04:56:07.000+00:00"}],"domain_name":"domainName","aef_id":"aefId","interface_descriptions":[{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":5248,"ipv4_addr":"ipv4Addr"},{"ipv6_addr":"ipv6Addr","security_methods":[None,None],"port":5248,"ipv4_addr":"ipv4Addr"}]}],"pub_api_path":{"ccf_ids":["ccfIds","ccfIds"]}}

    headers = {
    }
    response = client.request(
        "PUT",
        "/{apfId}/service-apis/{serviceApiId}".format(serviceApiId='service_api_id_example', apfId='apf_id_example'),
        headers=headers,
        json=service_api_description,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

