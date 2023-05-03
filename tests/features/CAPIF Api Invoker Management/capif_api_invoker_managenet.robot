*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Resource        /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagementRequests.robot
Resource    ../../resources/common.resource
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
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    access_token=${register_user_info['access_token']}

    # Check Results
    Check Response Variable Type And Values  ${resp}  201  APIInvokerEnrolmentDetails
    Check Location Header    ${resp}    ${LOCATION_INVOKER_RESOURCE_REGEX}

    # Store dummy signed certificate
    Store In File    ${INVOKER_USERNAME}.crt    ${resp.json()['onboardingInformation']['apiInvokerCertificate']}

Register NetApp Already Onboarded
    [Tags]    capif_api_invoker_management-2
    # Default Invoker Registration and Onboarding
    ${register_user_info}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_onboarding_url']}
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    access_token=${register_user_info['access_token']}

    # Check Results
    Check Response Variable Type And Values    ${resp}    403    ProblemDetails
    ...    status=403
    ...    title=Forbidden
    ...    detail=Invoker already registered
    ...    cause=Identical invoker public key

Update Onboarded NetApp
    [Tags]    capif_api_invoker_management-3
    ${new_notification_destination}=    Set Variable
    ...    http://${CAPIF_CALLBACK_IP}:${CAPIF_CALLBACK_PORT}/netapp_new_callback
    # Default Invoker Registration and Onboarding
    ${register_user_info}    ${url}    ${request_body}=    Invoker Default Onboarding

    Set To Dictionary
    ...    ${request_body}
    ...    notificationDestination=${new_notification_destination}

    ${resp}=    Put Request Capif
    ...    ${url.path}
    ...    ${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    200    APIInvokerEnrolmentDetails
    ...    notificationDestination=${new_notification_destination}

Update Not Onboarded NetApp
    [Tags]    capif_api_invoker_management-4
    # Default Invoker Registration and Onboarding
    ${register_user_info}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${resp}=    Put Request Capif
    ...    /api-invoker-management/v1/onboardedInvokers/${INVOKER_NOT_REGISTERED}
    ...    ${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    status=404
    ...    title=Not Found
    ...    detail=Please provide an existing Netapp ID
    ...    cause=Not exist NetappID

Offboard NetApp
    [Tags]    capif_api_invoker_management-5
    # Default Invoker Registration and Onboarding
    ${register_user_info}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${resp}=    Delete Request Capif
    ...    ${url.path}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Results
    Should Be Equal As Strings    ${resp.status_code}    204

Offboard Not Previously Onboarded NetApp
    [Tags]    capif_api_invoker_management-6
    # Default Invoker Registration and Onboarding
    ${register_user_info}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${resp}=    Delete Request Capif
    ...    /api-invoker-management/v1/onboardedInvokers/${INVOKER_NOT_REGISTERED}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    status=404
    ...    title=Not Found
    ...    detail=Please provide an existing Netapp ID
    ...    cause=Not exist NetappID

Update Onboarded NetApp Certificate
    [Tags]    capif_api_invoker_management-7
    ${new_notification_destination}=    Set Variable
    ...    http://${CAPIF_CALLBACK_IP}:${CAPIF_CALLBACK_PORT}/netapp_new_callback
    # Default Invoker Registration and Onboarding
    ${register_user_info}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${INVOKER_USERNAME_NEW}=   Set Variable     ${INVOKER_USERNAME}_NEW

    ${csr_request_new}=    Create User Csr    ${INVOKER_USERNAME_NEW}    invoker

    ${new_onboarding_notification_body}=    Create Onboarding Notification Body
    ...    http://${CAPIF_CALLBACK_IP}:${CAPIF_CALLBACK_PORT}/netapp_callback
    ...    ${csr_request_new}
    ...    ${INVOKER_USERNAME}

    Set To Dictionary
    ...    ${request_body}
    ...    onboardingInformation=${new_onboarding_notification_body['onboardingInformation']}

    ${resp}=    Put Request Capif
    ...    ${url.path}
    ...    ${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Check Response Variable Type And Values    ${resp}    200    APIInvokerEnrolmentDetails

    Store In File    ${INVOKER_USERNAME_NEW}.crt    ${resp.json()['onboardingInformation']['apiInvokerCertificate']}

    Set To Dictionary
    ...    ${request_body}
    ...    notificationDestination=${new_notification_destination}

    ${resp}=    Put Request Capif
    ...    ${url.path}
    ...    ${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME_NEW}

    # Check Results
    Check Response Variable Type And Values    ${resp}    200    APIInvokerEnrolmentDetails
    ...    notificationDestination=${new_notification_destination}
