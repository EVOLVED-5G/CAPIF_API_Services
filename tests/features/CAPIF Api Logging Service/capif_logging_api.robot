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
Create a log entry
    [Tags]    capif_api_logging_service-1
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
    ${resp}=    Post Request Capif
    ...    /api-invocation-logs/v1/${register_user_info['aef_id']}/logs
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AEF_PROVIDER_USERNAME}


    # Check Results
    Check Response Variable Type And Values    ${resp}    201    InvocationLog
    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_LOGGING_RESOURCE_REGEX}

Create a log entry invalid aefId
    [Tags]    capif_api_logging_service-2
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
    ${resp}=    Post Request Capif
    ...    /api-invocation-logs/v1/${AEF_ID_NOT_VALID}/logs
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AEF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    404   ProblemDetails
    ...    title=Not Found
    ...    status=404
    ...    detail=Exposer not exist
    ...    cause=Exposer id not found



Create a log entry invalid serviceApi
    [Tags]    capif_api_logging_service-3
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

    # Create Log Entry
    ${request_body}=  Create Log Entry Bad Service  ${register_user_info['aef_id']}  ${register_user_info_invoker['api_invoker_id']}
    ${resp}=    Post Request Capif
    ...    /api-invocation-logs/v1/${register_user_info['aef_id']}/logs
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AEF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    title=Not Found
    ...    status=404
    ...    detail=Service API not exist

Create a log entry invalid apiInvokerId
    [Tags]    capif_api_logging_service-4
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
    ${request_body}=  Create Log Entry  ${register_user_info['aef_id']}  ${API_INVOKER_NOT_VALID}   ${api_ids}  ${api_names}
    ${resp}=    Post Request Capif
    ...    /api-invocation-logs/v1/${register_user_info['aef_id']}/logs
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AEF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    title=Not Found
    ...    status=404
    ...    detail=Invoker not exist
    ...    cause=Invoker id not found


Create a log entry different aef_id in body
    [Tags]    capif_api_logging_service-5
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
    ${request_body}=  Create Log Entry  ${AEF_ID_NOT_VALID}  ${register_user_info_invoker['api_invoker_id']}  ${api_ids}  ${api_names}
    ${resp}=    Post Request Capif
    ...    /api-invocation-logs/v1/${register_user_info['aef_id']}/logs
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${AEF_PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
    ...    title=Unauthorized
    ...    status=401
    ...    detail=AEF id not matching in request and body
    ...    cause=Not identical AEF id

