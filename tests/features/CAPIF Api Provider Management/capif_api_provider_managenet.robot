*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Resource    ../../resources/common.resource
# Resource    /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagementRequests.robot
Library         /opt/robot-tests/tests/libraries/bodyRequests.py
Library         Process

Test Setup      Reset Testing Environment


*** Variables ***
${API_PROVIDER_NOT_REGISTERED}      notValid


*** Test Cases ***
Register Api Provider
    [Tags]    capif_api_provider_management-1
    # Register Exposer
    ${register_user_info}=    Publisher Default Registration

    # Create provider Registration Body
    ${request_body}=    Create Api Provider Enrolment Details Body
    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    201    APIProviderEnrolmentDetails
    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_PROVIDER_RESOURCE_REGEX}

Register Api Provider Already registered
    [Tags]    capif_api_provider_management-2
    ${register_user_info}=    Publisher Default Registration

    ${request_body}=    Create Api Provider Enrolment Details Body

    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}
    
    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_PROVIDER_RESOURCE_REGEX}

    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    403    ProblemDetails
    ...    status=403
    ...    title=Forbidden
    ...    detail=Provider already registered
    ...    cause=Identical provider reg sec

Update Registered Api Provider
    [Tags]    capif_api_provider_management-3
    ${register_user_info}=    Publisher Default Registration

    ${request_body}=    Create Api Provider Enrolment Details Body

    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_PROVIDER_RESOURCE_REGEX}

    ${request_body}=    Create Api Provider Enrolment Details Body   ROBOT_TESTING_MOD
    ${resp}=    Put Request Capif
    ...    ${resource_url.path}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    200    APIProviderEnrolmentDetails
    ...   apiProvDomInfo=ROBOT_TESTING_MOD

Update Not Registered Api Provider
    [Tags]    capif_api_provider_management-4
    ${register_user_info}=    Publisher Default Registration

    ${request_body}=    Create Api Provider Enrolment Details Body

    ${resp}=    Put Request Capif
    ...    /api-provider-management/v1/registrations/${API_PROVIDER_NOT_REGISTERED}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    status=404
    ...    title=Not Found
    ...    detail=Not Exist Provider Enrolment Details
    ...    cause=Not found registrations to send this api provider details


Partially Update Registered Api Provider
    [Tags]    capif_api_provider_management-5
    ${register_user_info}=    Publisher Default Registration

    ${request_body}=    Create Api Provider Enrolment Details Body

    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    201    APIProviderEnrolmentDetails
    ...    apiProvDomInfo=ROBOT_TESTING
    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_PROVIDER_RESOURCE_REGEX}

    ${request_body}=    Create Api Provider Enrolment Details Patch Body   ROBOT_TESTING_MOD

    ${resp}=    Patch Request Capif
    ...    ${resource_url.path}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    200    APIProviderEnrolmentDetails
    ...    apiProvDomInfo=ROBOT_TESTING_MOD


Partially Update Not Registered Api Provider
    [Tags]    capif_api_provider_management-6
    ${register_user_info}=    Publisher Default Registration

    ${request_body}=    Create Api Provider Enrolment Details Patch Body

    ${resp}=    Patch Request Capif
    ...    /api-provider-management/v1/registrations/${API_PROVIDER_NOT_REGISTERED}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    status=404
    ...    title=Not Found
    ...    detail=Not Exist Provider Enrolment Details
    ...    cause=Not found registrations to send this api provider details

Delete Registered Api Provider
    [Tags]    capif_api_provider_management-7
    ${register_user_info}=    Publisher Default Registration

    ${request_body}=    Create Api Provider Enrolment Details Body

    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Check Response Variable Type And Values    ${resp}    201    APIProviderEnrolmentDetails
    ...    apiProvDomInfo=ROBOT_TESTING
    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_PROVIDER_RESOURCE_REGEX}

    ${resp}=    Delete Request Capif
    ...    ${resource_url.path}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}
    
    # Check Results
    Status Should Be    204    ${resp}

Delete Not Registered Api Provider
    [Tags]    capif_api_provider_management-8
    ${register_user_info}=    Publisher Default Registration

    ${resp}=    Delete Request Capif
    ...    /api-provider-management/v1/registrations/${API_PROVIDER_NOT_REGISTERED}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    status=404
    ...    title=Not Found
    ...    detail=Not Exist Provider Enrolment Details
    ...    cause=Not found registrations to send this api provider details

