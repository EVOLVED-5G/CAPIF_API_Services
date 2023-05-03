*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Resource        ../../resources/common.resource
Library         /opt/robot-tests/tests/libraries/bodyRequests.py
Library         Process
Library         Collections

Test Setup      Reset Testing Environment


*** Variables ***
${API_PROVIDER_NOT_REGISTERED}      notValid


*** Test Cases ***
Register Api Provider
    [Tags]    capif_api_provider_management-1
    #Register Provider User An create Certificates for each function
    ${register_user_info}=    Register User At Jwt Auth Provider
    ...    username=${PROVIDER_USERNAME}    role=${PROVIDER_ROLE}

    # Create provider Registration Body
    ${apf_func_details}=    Create Api Provider Function Details
    ...    ${register_user_info['apf_username']}
    ...    ${register_user_info['apf_csr_request']}
    ...    APF
    ${aef_func_details}=    Create Api Provider Function Details
    ...    ${register_user_info['aef_username']}
    ...    ${register_user_info['aef_csr_request']}
    ...    AEF
    ${amf_func_details}=    Create Api Provider Function Details
    ...    ${register_user_info['amf_username']}
    ...    ${register_user_info['amf_csr_request']}
    ...    AMF
    ${api_prov_funcs}=    Create List    ${apf_func_details}    ${aef_func_details}    ${amf_func_details}

    ${request_body}=    Create Api Provider Enrolment Details Body
    ...    ${register_user_info['access_token']}
    ...    ${api_prov_funcs}

    # Register Provider
    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    access_token=${register_user_info['access_token']}

    # Check Results
    Check Response Variable Type And Values    ${resp}    201    APIProviderEnrolmentDetails
    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_PROVIDER_RESOURCE_REGEX}

    FOR    ${prov}    IN    @{resp.json()['apiProvFuncs']}
        Log Dictionary    ${prov}
        Store In File    ${prov['apiProvFuncInfo']}.crt    ${prov['regInfo']['apiProvCert']}
    END

Register Api Provider Already registered
    [Tags]    capif_api_provider_management-2
    ${register_user_info}=    Provider Default Registration

    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${register_user_info['provider_enrollment_details']}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    access_token=${register_user_info['access_token']}

    # Check Results
    Check Response Variable Type And Values    ${resp}    403    ProblemDetails
    ...    status=403
    ...    title=Forbidden
    ...    detail=Provider already registered
    ...    cause=Identical provider reg sec

Update Registered Api Provider
    [Tags]    capif_api_provider_management-3
    ${register_user_info}=    Provider Default Registration

    ${request_body}=    Set Variable    ${register_user_info['provider_enrollment_details']}

    Set To Dictionary    ${request_body}    apiProvDomInfo=ROBOT_TESTING_MOD

    ${resp}=    Put Request Capif
    ...    ${register_user_info['resource_url'].path}
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AMF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    200    APIProviderEnrolmentDetails
    ...    apiProvDomInfo=ROBOT_TESTING_MOD

Update Not Registered Api Provider
    [Tags]    capif_api_provider_management-4
    ${register_user_info}=    Provider Default Registration

    ${request_body}=    Set Variable    ${register_user_info['provider_enrollment_details']}

    ${resp}=    Put Request Capif
    ...    /api-provider-management/v1/registrations/${API_PROVIDER_NOT_REGISTERED}
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AMF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    status=404
    ...    title=Not Found
    ...    detail=Not Exist Provider Enrolment Details
    ...    cause=Not found registrations to send this api provider details

Partially Update Registered Api Provider
    [Tags]    capif_api_provider_management-5
    ${register_user_info}=    Provider Default Registration

    ${request_body}=    Create Api Provider Enrolment Details Patch Body    ROBOT_TESTING_MOD

    ${resp}=    Patch Request Capif
    ...    ${register_user_info['resource_url'].path}
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AMF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    200    APIProviderEnrolmentDetails
    ...    apiProvDomInfo=ROBOT_TESTING_MOD

Partially Update Not Registered Api Provider
    [Tags]    capif_api_provider_management-6
    ${register_user_info}=    Provider Default Registration

    ${request_body}=    Create Api Provider Enrolment Details Patch Body

    ${resp}=    Patch Request Capif
    ...    /api-provider-management/v1/registrations/${API_PROVIDER_NOT_REGISTERED}
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AMF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    status=404
    ...    title=Not Found
    ...    detail=Not Exist Provider Enrolment Details
    ...    cause=Not found registrations to send this api provider details

Delete Registered Api Provider
    [Tags]    capif_api_provider_management-7
    ${register_user_info}=    Provider Default Registration

    ${resp}=    Delete Request Capif
    ...    ${register_user_info['resource_url'].path}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AMF_PROVIDER_USERNAME}

    # Check Results
    Status Should Be    204    ${resp}

Delete Not Registered Api Provider
    [Tags]    capif_api_provider_management-8
    ${register_user_info}=    Provider Default Registration

    ${resp}=    Delete Request Capif
    ...    /api-provider-management/v1/registrations/${API_PROVIDER_NOT_REGISTERED}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AMF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    status=404
    ...    title=Not Found
    ...    detail=Not Exist Provider Enrolment Details
    ...    cause=Not found registrations to send this api provider details
