*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Resource        /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagementRequests.robot
Library         /opt/robot-tests/tests/libraries/bodyRequests.py
Library         Process
Library         Collections

Test Setup      Reset Testing Environment


*** Variables ***
${API_INVOKER_NOT_REGISTERED}       not-valid


*** Test Cases ***
Onboard NetApp
    [Tags]    capif_api_invoker_management-1
    #Register Netapp
    ${register_user_info}=    Register User At Jwt Auth
    ...    username=${INVOKER_USERNAME}    role=${INVOKER_ROLE}

    # Send Onboarding Request
    ${request_body}=    Create Onboarding Notification Body
    ...    http://${CAPIF_CALLBACK_IP}:${CAPIF_CALLBACK_PORT}/netapp_callback
    ...    ${register_user_info['csr_request']}
    ...    ${INVOKER_USERNAME}
    ${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_onboarding_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    access_token=${register_user_info['access_token']}

    Status Should Be    201    ${resp}
    Check Variable    ${resp.json()}    APIInvokerEnrolmentDetails
    # Store dummy signed certificate
    Store In File    ${INVOKER_USERNAME}.crt    ${resp.json()['onboardingInformation']['apiInvokerCertificate']}

Register NetApp Already Onboarded
    [Tags]    capif_api_invoker_management-2
    # Default Invoker Registration and Onboarding
    ${register_user_info}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_onboarding_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    access_token=${register_user_info['access_token']}

    Status Should Be    403    ${resp}
    Check Variable    ${resp.json()}    ProblemDetails

Update Onboarded NetApp
    [Tags]    capif_api_invoker_management-3
    # Default Invoker Registration and Onboarding
    ${register_user_info}    ${url}    ${request_body}=    Invoker Default Onboarding

    Set To Dictionary
    ...    ${request_body}
    ...    notificationDestination=http://${CAPIF_CALLBACK_IP}:${CAPIF_CALLBACK_PORT}/netapp_new_callback

    ${resp}=    Put Request Capif
    ...    ${url.path}
    ...    ${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    200    ${resp}
    Check Variable    ${resp.json()}    APIInvokerEnrolmentDetails

Update Not Onboarded NetApp
    [Tags]    capif_api_invoker_management-4
    # Default Invoker Registration and Onboarding
    ${register_user_info}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${resp}=    Put Request Capif
    ...    /api-invoker-management/v1/onboardedInvokers/${INVOKER_NOT_REGISTERED}
    ...    ${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    404    ${resp}
    Check Variable    ${resp.json()}    ProblemDetails

Offboard NetApp
    [Tags]    capif_api_invoker_management-5
    # Default Invoker Registration and Onboarding
    ${register_user_info}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${resp}=    Delete Request Capif
    ...    ${url.path}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Should Be Equal As Strings    ${resp.status_code}    204

Offboard Not Previously Onboarded NetApp
    [Tags]    capif_api_invoker_management-6
    # Default Invoker Registration and Onboarding
    ${register_user_info}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${resp}=    Delete Request Capif
    ...    /api-invoker-management/v1/onboardedInvokers/${INVOKER_NOT_REGISTERED}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    404    ${resp}
    Check Variable    ${resp.json()}    ProblemDetails

# CHECKING JMS
#     [Tags]    jms_test
#     [Setup]    NONE

#     Check Jms
