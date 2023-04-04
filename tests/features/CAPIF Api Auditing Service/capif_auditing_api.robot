*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Library         /opt/robot-tests/tests/libraries/bodyRequests.py
Library         Collections
Resource        /opt/robot-tests/tests/resources/common/basicRequests.robot
Resource        ../../resources/common.resource

Test Setup      Reset Testing Environment

*** Variables ***
${AEF_ID_NOT_VALID}             aef-example
${SERVICE_API_ID_NOT_VALID}     not-valid
${API_INVOKER_NOT_VALID}        not-valid
${NOTIFICATION_DESTINATION}     http://robot.testing:1080

*** Test Cases ***
Get Log Entry
    [Tags]    capif_api_auditing_service-1
    #Register APF
    ${register_user_info}=    Provider Default Registration

    # Publish one api
    Publish Service Api    ${register_user_info}

    #Register INVOKER
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${discover_response}=    Get Request Capif
    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    ${api_ids}   ${api_names}=    Get Api Ids And Names From Discover Response    ${discover_response}

    # Create Log Entry
    ${request_body}=  Create Log Entry  ${register_user_info['aef_id']}  ${register_user_info_invoker['api_invoker_id']}  ${api_ids}  ${api_names}
    ${resp_1}=    Post Request Capif
    ...    /api-invocation-logs/v1/${register_user_info['aef_id']}/logs
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${AEF_PROVIDER_USERNAME}


    ${resp_2}=    Get Request Capif
    ...    /logs/v1/apiInvocationLogs
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${AMF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp_2}    200    InvocationLog

Get a log entry without entry created
    [Tags]    capif_api_auditing_service-2
    #Register APF
    ${register_user_info}=    Provider Default Registration

    # Publish one api
    Publish Service Api    ${register_user_info}

    #Register INVOKER
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding


     ${resp_1}=  Get Request Capif
    ...    /logs/v1/apiInvocationLogs
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${AMF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp_1}    400   ProblemDetails
   
Get a log entry with invalid amfId
    [Tags]    capif_api_auditing_service-3
    #Register APF
    ${register_user_info}=    Provider Default Registration

    # Publish one api
    Publish Service Api    ${register_user_info}

    #Register INVOKER
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${discover_response}=    Get Request Capif
    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    ${api_ids}   ${api_names}=    Get Api Ids And Names From Discover Response    ${discover_response}

    # Create Log Entry
    ${request_body}=  Create Log Entry  ${register_user_info['aef_id']}  ${register_user_info_invoker['api_invoker_id']}  ${api_ids}  ${api_names}
    ${resp_1}=    Post Request Capif
    ...    /api-invocation-logs/v1/${AEF_ID_NOT_VALID}/logs
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${AEF_PROVIDER_USERNAME}


     ${resp_2}=    Get Request Capif
    ...    /logs/v1/apiInvocationLogs
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${AEF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp_2}    401   ProblemDetails
    ...    title=Unauthorized
    ...    status=401
    ...    detail=Role not authorized for this API route
    ...    cause=User role must be amf




