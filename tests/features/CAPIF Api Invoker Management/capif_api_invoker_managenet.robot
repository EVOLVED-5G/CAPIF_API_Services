*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Resource        /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagementRequests.robot
Library         /opt/robot-tests/tests/libraries/api_invoker_management/bodyRequests.py
Library         Process

Test Setup      Reset Testing Environment


*** Variables ***
${API_INVOKER_NOT_REGISTERED}       not-valid


*** Test Cases ***
TestJMS
    [Tags]    jms_test
    [Teardown]  Testing Teardown

    ${username}=    Set Variable    ROBOT_TESTING_INVOKER
    ${role}=    Set Variable    invoker

    #Register Netapp
    ${access_token}
    ...    ${netappID}
    ...    ${ccf_onboarding_url}
    ...    ${ccf_discover_url}
    ...    ${csr_request}=
    ...    Register User At Jwt Auth
    ...    username=${username}  role=${INVOKER_ROLE}

    ${capif_ip}=    Set Variable    capifcore
    ${capif_callback_ip}=    Set Variable    host.docker.internal
    ${capif_callback_port}=    Set Variable    8086

    # On Boarding
    ${request_body}=    Create Onboarding Notification Body
    ...    http://${capif_callback_ip}:${capif_callback_port}/netapp_callback
    ...    ${csr_request}
    ...    ${username}

    ${resp}=    Post Request Capif
    ...    ${ccf_onboarding_url}
    ...    json=${request_body}
    ...    server=https://${capif_ip}/
    ...    verify=ca.crt
    Status Should Be    201    ${resp}

    ${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

    # Store dummy signede certificate
    Store In File    ${username}.crt    ${resp.json()['onboardingInformation']['apiInvokerCertificate']}

    # Execute discover
    ${resp}=    Get Request Capif
    ...    ${ccf_discover_url}${api_invoker_id}
    ...    server=https://${capif_ip}/
    ...    verify=ca.crt
    ...    cert=${{ ('${username}.crt','${username}.key') }}
    # ...    cert=${cert}
    Status Should Be    200    ${resp}

Register NetApp
    [Tags]    capif_api_invoker_management-1

    ${request_body}=    Create Onboarding Notification Body
    ${resp}=    Post Request Capif
    ...    /api-invoker-management/v1/onboardedInvokers
    ...    ${request_body}

    Should Be Equal As Strings    ${resp.status_code}    201

Register NetApp Already registered
    [Tags]    capif_api_invoker_management-2

    ${request_body}=    Create Onboarding Notification Body
    ${resp}=    Post Request Capif
    ...    /api-invoker-management/v1/onboardedInvokers
    ...    ${request_body}

    Should Be Equal As Strings    ${resp.status_code}    201

    ${resp}=    Post Request Capif    /api-invoker-management/v1/onboardedInvokers    ${request_body}

    Should Be Equal As Strings    ${resp.status_code}    403

Update Registered NetApp
    [Tags]    capif_api_invoker_management-3

    ${request_body}=    Create Onboarding Notification Body
    ${resp}=    Post Request Capif
    ...    /api-invoker-management/v1/onboardedInvokers
    ...    ${request_body}

    Should Be Equal As Strings    ${resp.status_code}    201

    ${url}=    Parse Url    ${resp.headers['Location']}

    ${resp}=    Put Request Capif    ${url.path}    ${request_body}    server=${NGINX_HOSTNAME}

    Should Be Equal As Strings    ${resp.status_code}    200

Update Not Registered NetApp
    [Tags]    capif_api_invoker_management-4

    ${api_invoker_id}=    Set Variable    ${API_INVOKER_NOT_REGISTERED}

    ${request_body}=    Create Onboarding Notification Body
    ${resp}=    Put Request Capif
    ...    /api-invoker-management/v1/onboardedInvokers/${api_invoker_id}
    ...    ${request_body}

    Should Be Equal As Strings    ${resp.status_code}    404

Delete Registered NetApp
    [Tags]    capif_api_invoker_management-5

    ${request_body}=    Create Onboarding Notification Body
    ${resp}=    Post Request Capif
    ...    /api-invoker-management/v1/onboardedInvokers
    ...    ${request_body}

    Should Be Equal As Strings    ${resp.status_code}    201

    ${url}=    Parse Url    ${resp.headers['Location']}

    ${request_body}=    Create Onboarding Notification Body
    ${resp}=    Delete Request Capif    ${url.path}    server=${NGINX_HOSTNAME}

    Should Be Equal As Strings    ${resp.status_code}    204

Delete Not Registered NetApp
    [Tags]    capif_api_invoker_management-6

    ${api_invoker_id}=    Set Variable    ${API_INVOKER_NOT_REGISTERED}

    ${request_body}=    Create Onboarding Notification Body
    ${resp}=    Delete Request Capif
    ...    /api-invoker-management/v1/onboardedInvokers/${api_invoker_id}

    Should Be Equal As Strings    ${resp.status_code}    404


*** Keywords ***
Testing Teardown
    ${result}=    Run Process    ls
    Log    ${result.stdout}
    ${result}=    Run Process    cp    -vvv    *.crt    /opt/robot-tests/results/
    Log    ${result.stdout}
    ${result}=    Run Process    cp    -vvv    *.key    /opt/robot-tests/results/
    Log    ${result.stdout}
    ${result}=    Run Process    cp    -vvv    *.csr    /opt/robot-tests/results/
    Log    ${result.stdout}


