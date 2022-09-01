*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
# Resource    /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagementRequests.robot
Library         /opt/robot-tests/tests/libraries/bodyRequests.py
Library         Process

Test Setup      Reset Testing Environment


*** Variables ***
${API_PROVIDER_NOT_REGISTERED}       notValid


*** Test Cases ***
Register Api Provider
    [Tags]    capif_api_provider_management-1
    ${request_body}=    Create Api Provider Enrolment Details Body

    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/

    Status Should Be    201    ${resp}

    ${location_url}=    Parse Url    ${resp.headers['Location']}
    Log    ${location_url.path}

    Should Match Regexp    ${location_url.path}    ^/api-provider-management/v1/registrations/[0-9a-zA-Z]+

Register Api Provider Already registered
    [Tags]    capif_api_provider_management-2
    ${request_body}=    Create Api Provider Enrolment Details Body

    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/

    Status Should Be    201    ${resp}

    ${location_url}=    Parse Url    ${resp.headers['Location']}
    Log    ${location_url.path}

    Should Match Regexp    ${location_url.path}    ^/api-provider-management/v1/registrations/[0-9a-zA-Z]+

    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/

    Status Should Be    403    ${resp}

Update Registered Api Provider
    [Tags]    capif_api_provider_management-3
    ${request_body}=    Create Api Provider Enrolment Details Body

    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/

    Status Should Be    201    ${resp}

    ${location_url}=    Parse Url    ${resp.headers['Location']}
    Log    ${location_url.path}

    Should Match Regexp    ${location_url.path}    ^/api-provider-management/v1/registrations/[0-9a-zA-Z]+

    ${registration_id}=    Get Registration Id    ${location_url.path}

    ${resp}=    Put Request Capif
    ...    ${location_url.path}    
    ...    json=${request_body}
    ...    server=http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/

    Status Should Be    200    ${resp}

Update Not Registered Api Provider
    [Tags]    capif_api_provider_management-4
    ${request_body}=    Create Api Provider Enrolment Details Body

    ${resp}=    Put Request Capif
    ...    /api-provider-management/v1/registrations/${API_PROVIDER_NOT_REGISTERED}
    ...    json=${request_body}
    ...    server=http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/

    Status Should Be    404    ${resp}

Partially Update Registered Api Provider
    [Tags]    capif_api_provider_management-5
    ${request_body}=    Create Api Provider Enrolment Details Body

    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/

    Status Should Be    201    ${resp}
    # Store dummy signede certificate
    ${location_url}=    Parse Url    ${resp.headers['Location']}
    Log    ${location_url.path}

    Should Match Regexp    ${location_url.path}    ^/api-provider-management/v1/registrations/[0-9a-zA-Z]+

    ${request_body}=    Create Api Provider Enrolment Details Patch Body

    ${resp}=    Patch Request Capif
    ...    ${location_url.path}    
    ...    json=${request_body}
    ...    server=http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/

    Status Should Be    200    ${resp}

Partially Update Not Registered Api Provider
    [Tags]    capif_api_provider_management-6
    ${request_body}=    Create Api Provider Enrolment Details Patch Body

    ${resp}=    Patch Request Capif
    ...    /api-provider-management/v1/registrations/${API_PROVIDER_NOT_REGISTERED}
    ...    json=${request_body}
    ...    server=http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/

    Status Should Be    404    ${resp}

Delete Registered Api Provider
    [Tags]    capif_api_provider_management-7
    ${request_body}=    Create Api Provider Enrolment Details Body

    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/

    Status Should Be    201    ${resp}

    ${location_url}=    Parse Url    ${resp.headers['Location']}

    ${resp}=    Delete Request Capif
    ...    ${location_url.path}
    ...    server=http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/

    Status Should Be    204    ${resp}

Delete Not Registered Api Provider
    [Tags]    capif_api_provider_management-8

    ${resp}=    Delete Request Capif
    ...    /api-provider-management/v1/registrations/${API_PROVIDER_NOT_REGISTERED}
    ...    server=http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/

    Status Should Be    404    ${resp}
