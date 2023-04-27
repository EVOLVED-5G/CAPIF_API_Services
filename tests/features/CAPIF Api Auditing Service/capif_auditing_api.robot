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
${API_VERSION_VALID}            v1
${API_VERSION_NOT_VALID}        v58

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
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    ${api_ids}   ${api_names}=    Get Api Ids And Names From Discover Response    ${discover_response}

    # Create Log Entry
    ${request_body}=  Create Log Entry  ${register_user_info['aef_id']}  ${register_user_info_invoker['api_invoker_id']}  ${api_ids}  ${api_names}
    ${resp_1}=    Post Request Capif
    ...    /api-invocation-logs/v1/${register_user_info['aef_id']}/logs
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AEF_PROVIDER_USERNAME}


    ${resp_2}=    Get Request Capif
    ...    /logs/v1/apiInvocationLogs?aef-id=${register_user_info['aef_id']}&api-invoker-id=${register_user_info_invoker['api_invoker_id']}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AMF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp_2}    200    InvocationLog
    Length Should Be   ${resp_2.json()["logs"]}  2

Get a log entry without entry created
    [Tags]    capif_api_auditing_service-2
    #Register APF
    ${register_user_info}=    Provider Default Registration

    # Publish one api
    Publish Service Api    ${register_user_info}

    #Register INVOKER
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding


     ${resp_1}=  Get Request Capif
    ...    /logs/v1/apiInvocationLogs?aef-id=${register_user_info['aef_id']}&api-invoker-id=${register_user_info_invoker['api_invoker_id']}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AMF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp_1}    404   ProblemDetails
    ...    title=Not Found
    ...    status=404
    ...    detail=aefId or/and apiInvokerId do not match any InvocationLogs
    ...    cause=No log invocations found


Get a log entry withut aefid and apiInvokerId
    [Tags]    capif_api_auditing_service-3
    #Register APF
    ${register_user_info}=    Provider Default Registration

    # Publish one api
    Publish Service Api    ${register_user_info}

    #Register INVOKER
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${discover_response}=    Get Request Capif
    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    ${api_ids}   ${api_names}=    Get Api Ids And Names From Discover Response    ${discover_response}

    # Create Log Entry
    ${request_body}=  Create Log Entry  ${register_user_info['aef_id']}  ${register_user_info_invoker['api_invoker_id']}  ${api_ids}  ${api_names}
    ${resp_1}=    Post Request Capif
    ...    /api-invocation-logs/v1/${AEF_ID_NOT_VALID}/logs
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AEF_PROVIDER_USERNAME}


     ${resp_2}=    Get Request Capif
    ...    /logs/v1/apiInvocationLogs
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AMF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp_2}    400   ProblemDetails
    ...    title=Bad Request
    ...    status=400
    ...    detail=aef_id and api_invoker_id parameters are mandatory
    ...    cause=Mandatory parameters missing


Get Log Entry with apiVersion filter
    [Tags]    capif_api_auditing_service-4
    #Register APF
    ${register_user_info}=    Provider Default Registration

    # Publish one api
    Publish Service Api    ${register_user_info}

    #Register INVOKER
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${discover_response}=    Get Request Capif
    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    ${api_ids}   ${api_names}=    Get Api Ids And Names From Discover Response    ${discover_response}

    # Create Log Entry
    ${request_body}=  Create Log Entry  ${register_user_info['aef_id']}  ${register_user_info_invoker['api_invoker_id']}  ${api_ids}  ${api_names}
    ${resp_1}=    Post Request Capif
    ...    /api-invocation-logs/v1/${register_user_info['aef_id']}/logs
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AEF_PROVIDER_USERNAME}


    ${resp_2}=    Get Request Capif
    ...    /logs/v1/apiInvocationLogs?aef-id=${register_user_info['aef_id']}&api-invoker-id=${register_user_info_invoker['api_invoker_id']}&api-version=${API_VERSION_VALID} 
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AMF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp_2}    200    InvocationLog
    Length Should Be   ${resp_2.json()["logs"]}  1

Get Log Entry with no exist apiVersion filter 
    [Tags]    capif_api_auditing_service-5
    #Register APF
    ${register_user_info}=    Provider Default Registration

    # Publish one api
    Publish Service Api    ${register_user_info}

    #Register INVOKER
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${discover_response}=    Get Request Capif
    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    ${api_ids}   ${api_names}=    Get Api Ids And Names From Discover Response    ${discover_response}

    # Create Log Entry
    ${request_body}=  Create Log Entry  ${register_user_info['aef_id']}  ${register_user_info_invoker['api_invoker_id']}  ${api_ids}  ${api_names}
    ${resp_1}=    Post Request Capif
    ...    /api-invocation-logs/v1/${register_user_info['aef_id']}/logs
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AEF_PROVIDER_USERNAME}


    ${resp_2}=    Get Request Capif
    ...    /logs/v1/apiInvocationLogs?aef-id=${register_user_info['aef_id']}&api-invoker-id=${register_user_info_invoker['api_invoker_id']}&api-version=${API_VERSION_NOT_VALID} 
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AMF_PROVIDER_USERNAME}

    # Check Results
   # Check Results
    Check Response Variable Type And Values    ${resp_2}    404   ProblemDetails
    ...    title=Not Found
    ...    status=404
    ...    detail=Parameters do not match any log entry
    ...    cause=No logs found




