# coding: utf-8

from fastapi.testclient import TestClient


from api_provider_management.models.api_provider_enrolment_details import APIProviderEnrolmentDetails  # noqa: F401
from api_provider_management.models.problem_details import ProblemDetails  # noqa: F401


def test_registrations_post(client: TestClient):
    """Test case for registrations_post

    
    """
    api_provider_enrolment_details = {"reg_sec":"regSec","api_prov_funcs":[{"api_prov_func_id":"apiProvFuncId","api_prov_func_info":"apiProvFuncInfo","reg_info":{"api_prov_cert":"apiProvCert","api_prov_pub_key":"apiProvPubKey"}},{"api_prov_func_id":"apiProvFuncId","api_prov_func_info":"apiProvFuncInfo","reg_info":{"api_prov_cert":"apiProvCert","api_prov_pub_key":"apiProvPubKey"}}],"fail_reason":"failReason","api_prov_dom_id":"apiProvDomId","api_prov_dom_info":"apiProvDomInfo","supp_feat":"suppFeat"}

    headers = {
    }
    response = client.request(
        "POST",
        "/registrations",
        headers=headers,
        json=api_provider_enrolment_details,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_registrations_registration_id_delete(client: TestClient):
    """Test case for registrations_registration_id_delete

    
    """

    headers = {
    }
    response = client.request(
        "DELETE",
        "/registrations/{registrationId}".format(registrationId='registration_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_registrations_registration_id_put(client: TestClient):
    """Test case for registrations_registration_id_put

    
    """
    api_provider_enrolment_details = {"reg_sec":"regSec","api_prov_funcs":[{"api_prov_func_id":"apiProvFuncId","api_prov_func_info":"apiProvFuncInfo","reg_info":{"api_prov_cert":"apiProvCert","api_prov_pub_key":"apiProvPubKey"}},{"api_prov_func_id":"apiProvFuncId","api_prov_func_info":"apiProvFuncInfo","reg_info":{"api_prov_cert":"apiProvCert","api_prov_pub_key":"apiProvPubKey"}}],"fail_reason":"failReason","api_prov_dom_id":"apiProvDomId","api_prov_dom_info":"apiProvDomInfo","supp_feat":"suppFeat"}

    headers = {
    }
    response = client.request(
        "PUT",
        "/registrations/{registrationId}".format(registrationId='registration_id_example'),
        headers=headers,
        json=api_provider_enrolment_details,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

