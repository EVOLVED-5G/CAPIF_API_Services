*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Library         /opt/robot-tests/tests/libraries/bodyRequests.py
Library         Collections
Resource        /opt/robot-tests/tests/resources/common/basicRequests.robot
Resource        ../../resources/common.resource
Resource        ../../resources/performance.resource

Test Setup      Reset Testing Environment

*** Variables ***
${AEF_ID_NOT_VALID}             aef-example
${SERVICE_API_ID_NOT_VALID}     not-valid
${API_INVOKER_NOT_VALID}        not-valid
${NOTIFICATION_DESTINATION}     http://robot.testing:1080
${API_VERSION_VALID}            v1
${API_VERSION_NOT_VALID}        v58

*** Test Cases ***
Get Log Entry Performance
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


    ${success}=     Set Variable    ${0}
    ${average}=     Set Variable    ${0}

    FOR     ${index}    IN RANGE    ${ITERATIONS}
        Log To Console      \nIteration: ${index}

        ${resp_2}=    Get Request Capif
        ...    /logs/v1/apiInvocationLogs?aef-id=${register_user_info['aef_id']}&api-invoker-id=${register_user_info_invoker['api_invoker_id']}
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${AMF_PROVIDER_USERNAME}

        # Check Results
        Check Response Variable Type And Values    ${resp_2}    200    InvocationLog
        Length Should Be   ${resp_2.json()["logs"]}  2

        ${success}       ${average}      Handle Timing       ${resp_2.elapsed}     ${index}    ${average}      ${success}
    END

    Handle End Results      ${success}      ${average}


Get a log entry without entry created performance
    [Tags]    capif_api_auditing_service-2
    #Register APF
    ${register_user_info}=    Provider Default Registration

    # Publish one api
    Publish Service Api    ${register_user_info}

    #Register INVOKER
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${success}=     Set Variable    ${0}
    ${average}=     Set Variable    ${0}

    FOR     ${index}    IN RANGE    ${ITERATIONS}
        Log To Console      \nIteration: ${index}

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

        ${success}       ${average}      Handle Timing       ${resp_1.elapsed}     ${index}    ${average}      ${success}
    END

    Handle End Results      ${success}      ${average}
