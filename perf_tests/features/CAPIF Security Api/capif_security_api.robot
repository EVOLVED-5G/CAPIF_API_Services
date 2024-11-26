*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Library         /opt/robot-tests/tests/libraries/bodyRequests.py
Library         Collections
Resource        /opt/robot-tests/tests/resources/common/basicRequests.robot
Resource        ../../resources/common.resource
Resource        ../../resources/performance.resource

Test Setup      Reset Testing Environment


*** Variables ***
${APF_ID_NOT_VALID}             apf-example
${SERVICE_API_ID_NOT_VALID}     not-valid
${API_INVOKER_NOT_VALID}        not-valid
${NOTIFICATION_DESTINATION}     http://robot.testing:1080


*** Test Cases ***
Create a security context for an API invoker Performance
    [Tags]    capif_security_api-1
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Register APF
    ${register_user_info_publisher}=    Provider Default Registration

    ${success}=     Set Variable    ${0}
    ${average}=     Set Variable    ${0}

    FOR     ${index}    IN RANGE    ${ITERATIONS}
        Log To Console      \nIteration: ${index}
        # Create Security Context
        ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
        ${resp}=    Put Request Capif
        ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
        ...    json=${request_body}
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${INVOKER_USERNAME}

        # Check Results
        Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
        ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_SECURITY_RESOURCE_REGEX}

        # Remove Security Context
        ${delete}=    Delete Request Capif
        ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${AEF_PROVIDER_USERNAME}

        Status Should Be    204    ${delete}

        ${success}       ${average}      Handle Timing       ${resp.elapsed}     ${index}    ${average}      ${success}
    END

    Handle End Results      ${success}      ${average}

#Create a security context for an API invoker with Provider role
#    [Tags]    capif_security_api-2
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    # Register Provider
#    ${register_user_info_publisher}=    Provider Default Registration
#
#    # Create Security Context
#    ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${AEF_PROVIDER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
#    ...    title=Unauthorized
#    ...    status=401
#    ...    detail=Role not authorized for this API route
#    ...    cause=User role must be invoker

#Create a security context for an API invoker with Provider entity role and invalid apiInvokerId
#    [Tags]    capif_security_api-3
#    # Register APF
#    ${register_user_info_publisher}=    Provider Default Registration
#
#    # Create Security Context
#    ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${AEF_PROVIDER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
#    ...    title=Unauthorized
#    ...    status=401
#    ...    detail=Role not authorized for this API route
#    ...    cause=User role must be invoker
#
#Create a security context for an API invoker with Invalid apiInvokerID
#    [Tags]    capif_security_api-4
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
#    ...    title=Not Found
#    ...    status=404
#    ...    detail=Invoker not found
#    ...    cause=API Invoker not exists or invalid ID

Retrieve the Security Context of an API Invoker Performance
    [Tags]    capif_security_api-5
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_SECURITY_RESOURCE_REGEX}

    ${service_security_context}=    Set Variable    ${resp.json()}

    # Register APF
    ${register_user_info_publisher}=    Provider Default Registration
    # Retrieve Security context can setup by parameters if authenticationInfo and authorizationInfo are needed at response.
    # ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}?authenticationInfo=true&authorizationInfo=true

    ${success}=     Set Variable    ${0}
    ${average}=     Set Variable    ${0}

    FOR     ${index}    IN RANGE    ${ITERATIONS}
        Log To Console      \nIteration: ${index}

        ${resp}=    Get Request Capif
        ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${AEF_PROVIDER_USERNAME}

        # Check Results
        Check Response Variable Type And Values    ${resp}    200    ServiceSecurity

        ${service_security_context_filtered}=    Remove Keys From Object
        ...    ${service_security_context}
        ...    authenticationInfo
        ...    authorizationInfo

        Dictionaries Should Be Equal    ${resp.json()}    ${service_security_context_filtered}

        ${success}       ${average}      Handle Timing       ${resp.elapsed}     ${index}    ${average}      ${success}
    END

    Handle End Results      ${success}      ${average}


#Retrieve the Security Context of an API Invoker with invalid apiInvokerID
#    [Tags]    capif_security_api-6
#    # Register APF
#    ${register_user_info_publisher}=    Provider Default Registration
#
#    ${resp}=    Get Request Capif
#    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${AEF_PROVIDER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
#    ...    title=Not Found
#    ...    status=404
#    ...    detail=Invoker not found
#    ...    cause=API Invoker not exists or invalid ID

#Retrieve the Security Context of an API Invoker with invalid apfId
#    [Tags]    capif_security_api-7
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
#
#    # We will request information using invoker user, that is not allowed
#    ${resp}=    Get Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
#    ...    title=Unauthorized
#    ...    status=401
#    ...    detail=Role not authorized for this API route
#    ...    cause=User role must be aef

Delete the Security Context of an API Invoker Delete
    [Tags]    capif_security_api-8
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Register APF
    ${register_user_info_publisher}=    Provider Default Registration

    ${success}=     Set Variable    ${0}
    ${average}=     Set Variable    ${0}

    FOR     ${index}    IN RANGE    ${ITERATIONS}
        Log To Console      \nIteration: ${index}
        ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
        ${resp}=    Put Request Capif
        ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
        ...    json=${request_body}
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${INVOKER_USERNAME}

        Check Response Variable Type And Values    ${resp}    201    ServiceSecurity

        # Remove Security Context
        ${resp}=    Delete Request Capif
        ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${AEF_PROVIDER_USERNAME}

        Status Should Be    204    ${resp}

        ${success}       ${average}      Handle Timing       ${resp.elapsed}     ${index}    ${average}      ${success}
    END

    Handle End Results      ${success}      ${average}


#Delete the Security Context of an API Invoker with Invoker entity role
#    [Tags]    capif_security_api-9
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
#
#    ${resp}=    Delete Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    # Check Result
#    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
#    ...    title=Unauthorized
#    ...    status=401
#    ...    detail=Role not authorized for this API route
#    ...    cause=User role must be aef

#Delete the Security Context of an API Invoker with Invoker entity role and invalid apiInvokerID
#    [Tags]    capif_security_api-10
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    ${resp}=    Delete Request Capif
#    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    # Check Result
#    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
#    ...    title=Unauthorized
#    ...    status=401
#    ...    detail=Role not authorized for this API route
#    ...    cause=User role must be aef
#
#Delete the Security Context of an API Invoker with invalid apiInvokerID
#    [Tags]    capif_security_api-11
#    # Register Provider
#    ${register_user_info_publisher}=    Provider Default Registration
#
#    ${resp}=    Delete Request Capif
#    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${AEF_PROVIDER_USERNAME}
#
#    # Check Result
#    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
#    ...    title=Not Found
#    ...    status=404
#    ...    detail=Invoker not found
#    ...    cause=API Invoker not exists or invalid ID

Update the Security Context of an API Invoker Performance
    [Tags]    capif_security_api-12
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Register Provider
    ${register_user_info_publisher}=    Provider Default Registration

    ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity

    # Store Initial Security Context
    #${security_context}=    Set Variable    ${resp.json()}

    ${success}=     Set Variable    ${0}
    ${average}=     Set Variable    ${0}

    FOR     ${index}    IN RANGE    ${ITERATIONS}
        Log To Console      \nIteration: ${index}

        # Update Security Context
        ${request_body}=    Create Service Security Body    http://robot.testing_${index}
        ${resp}=    Post Request Capif
        ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}/update
        ...    json=${request_body}
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${INVOKER_USERNAME}

        Check Response Variable Type And Values    ${resp}    200    ServiceSecurity

        ${success}       ${average}      Handle Timing       ${resp.elapsed}     ${index}    ${average}      ${success}
    END

    Handle End Results      ${success}      ${average}

#Update the Security Context of an API Invoker with Provider entity role
#    [Tags]    capif_security_api-13
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
#
#    #Register Provider
#    ${register_user_info_publisher}=    Provider Default Registration
#
#    ${resp}=    Post Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}/update
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${AEF_PROVIDER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
#    ...    title=Unauthorized
#    ...    status=401
#    ...    detail=Role not authorized for this API route
#    ...    cause=User role must be invoker

#Update the Security Context of an API Invoker with AEF entity role and invalid apiInvokerId
#    [Tags]    capif_security_api-14
#    #Register Provider
#    ${register_user_info_publisher}=    Provider Default Registration
#
#    ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
#    ${resp}=    Post Request Capif
#    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}/update
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${AEF_PROVIDER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
#    ...    title=Unauthorized
#    ...    status=401
#    ...    detail=Role not authorized for this API route
#    ...    cause=User role must be invoker
#
#Update the Security Context of an API Invoker with invalid apiInvokerID
#    [Tags]    capif_security_api-15
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
#    ${resp}=    Post Request Capif
#    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}/update
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    # Check Result
#    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
#    ...    title=Not Found
#    ...    status=404
#    ...    detail=Invoker not found
#    ...    cause=API Invoker not exists or invalid ID

Revoke the authorization of the API invoker for APIs Performance
    [Tags]    capif_security_api-16
    # Register APF
    ${register_user_info_provider}=    Provider Default Registration
    ${api_name}=    Set Variable    service_1

    # Register One Service
    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info_provider}
    ...    ${api_name}

    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Test
    ${discover_response}=    Get Request Capif
    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}&aef-id=${register_user_info_provider['aef_id']}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Check Response Variable Type And Values    ${discover_response}    200    DiscoveredAPIs

    ${api_ids}=    Get Api Ids From Discover Response    ${discover_response}

    ${success}=     Set Variable    ${0}
    ${average}=     Set Variable    ${0}

    FOR     ${index}    IN RANGE    ${ITERATIONS}
        Log To Console      \nIteration: ${index}

        # create Security Context
        ${request_body}=    Create Service Security From Discover Response
        ...    http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/test
        ...    ${discover_response}
        ${resp}=    Put Request Capif
        ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
        ...    json=${request_body}
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${INVOKER_USERNAME}

        Check Response Variable Type And Values    ${resp}    201    ServiceSecurity

        # Revoke Security Context by Provider
        ${request_body}=    Create Security Notification Body
        ...    ${register_user_info_invoker['api_invoker_id']}
        ...    ${api_ids}
        ${resp}=    Post Request Capif
        ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}/delete
        ...    json=${request_body}
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${AEF_PROVIDER_USERNAME}

        # Check Results
        Status Should Be    204    ${resp}

        ${success}       ${average}      Handle Timing       ${resp.elapsed}     ${index}    ${average}      ${success}
    END

    Handle End Results      ${success}      ${average}

#Revoke the authorization of the API invoker for APIs without valid apfID.
#    [Tags]    capif_security_api-17
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
#
#    ${security_context}=    Set Variable    ${resp.json()}
#
#    # Register Provider
#    ${register_user_info_publisher}=    Provider Default Registration
#
#    # Revoke Security Context by Invoker
#    ${request_body}=    Create Security Notification Body    ${register_user_info_invoker['api_invoker_id']}    1234
#    ${resp}=    Post Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}/delete
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
#    ...    title=Unauthorized
#    ...    status=401
#    ...    detail=Role not authorized for this API route
#    ...    cause=User role must be aef
#
#    ${resp}=    Get Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${AEF_PROVIDER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    200    ServiceSecurity
#    ${security_context_filtered}=    Remove Keys From Object
#    ...    ${security_context}
#    ...    authenticationInfo
#    ...    authorizationInfo
#    Dictionaries Should Be Equal    ${resp.json()}    ${security_context_filtered}
#
#Revoke the authorization of the API invoker for APIs with invalid apiInvokerId
#    [Tags]    capif_security_api-18
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    ${request_body}=    Create Service Security Body    ${NOTIFICATION_DESTINATION}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
#
#    ${security_context}=    Set Variable    ${resp.json()}
#
#    #Register Provider
#    ${register_user_info_publisher}=    Provider Default Registration
#
#    ${request_body}=    Create Security Notification Body    ${API_INVOKER_NOT_VALID}    1234
#    ${resp}=    Post Request Capif
#    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}/delete
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${AEF_PROVIDER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
#    ...    title=Not Found
#    ...    status=404
#    ...    detail=Invoker not found
#    ...    cause=API Invoker not exists or invalid ID
#
#    ${resp}=    Get Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}?authenticationInfo=true&authorizationInfo=true
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${AEF_PROVIDER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    200    ServiceSecurity
#    Dictionaries Should Be Equal    ${resp.json()}    ${security_context}

Retrieve access token Performance
    [Tags]    capif_security_api-19
    # Register APF
    ${register_user_info_provider}=    Provider Default Registration
    ${api_name}=    Set Variable    service_1

    # Register One Service
    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info_provider}
    ...    ${api_name}

    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Test
    ${discover_response}=    Get Request Capif
    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Check Response Variable Type And Values    ${discover_response}    200    DiscoveredAPIs

    # create Security Context
    ${request_body}=    Create Service Security From Discover Response
    ...    ${NOTIFICATION_DESTINATION}
    ...    ${discover_response}
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity

    # Retrieve Token from CCF
    ${scope}=    Create Scope    ${register_user_info_provider['aef_id']}    ${api_name}
    ${request_body}=    Create Access Token Req Body    ${register_user_info_invoker['api_invoker_id']}    ${scope}

    ${success}=     Set Variable    ${0}
    ${average}=     Set Variable    ${0}

    FOR     ${index}    IN RANGE    ${ITERATIONS}
        Log To Console      \nIteration: ${index}

        ${resp}=    Post Request Capif
        ...    /capif-security/v1/securities/${register_user_info_invoker['api_invoker_id']}/token
        ...    data=${request_body}
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${INVOKER_USERNAME}

        # Check Results
        Check Response Variable Type And Values    ${resp}    200    AccessTokenRsp
        ...    token_type=Bearer

        Should Not Be Empty    ${resp.json()['access_token']}

        ${success}       ${average}      Handle Timing       ${resp.elapsed}     ${index}    ${average}      ${success}
    END

    Handle End Results      ${success}      ${average}

#Retrieve access token by Provider
#    [Tags]    capif_security_api-20
#    # Register APF
#    ${register_user_info_provider}=    Provider Default Registration
#    ${api_name}=    Set Variable    service_1
#
#    # Register One Service
#    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
#    ...    ${register_user_info_provider}
#    ...    ${api_name}
#
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    # Test
#    ${discover_response}=    Get Request Capif
#    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${discover_response}    200    DiscoveredAPIs
#
#    # create Security Context
#    ${request_body}=    Create Service Security From Discover Response
#    ...    ${NOTIFICATION_DESTINATION}
#    ...    ${discover_response}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
#
#    # Retrieve Token from CCF
#    ${scope}=    Create Scope    ${register_user_info_provider['aef_id']}    ${api_name}
#    ${request_body}=    Create Access Token Req Body    ${register_user_info_invoker['api_invoker_id']}    ${scope}
#    ${resp}=    Post Request Capif
#    ...    /capif-security/v1/securities/${register_user_info_invoker['api_invoker_id']}/token
#    ...    data=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${AEF_PROVIDER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    401    AccessTokenErr
#    ...    error=unauthorized_client
#    ...    error_description=Role not authorized for this API route

#Retrieve access token by Provider with invalid apiInvokerId
#    [Tags]    capif_security_api-21
#    # Register APF
#    ${register_user_info_provider}=    Provider Default Registration
#    ${api_name}=    Set Variable    service_1
#
#    # Register One Service
#    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
#    ...    ${register_user_info_provider}
#    ...    ${api_name}
#
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    # Test
#    ${discover_response}=    Get Request Capif
#    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${discover_response}    200    DiscoveredAPIs
#
#    # create Security Context
#    ${request_body}=    Create Service Security From Discover Response
#    ...    ${NOTIFICATION_DESTINATION}
#    ...    ${discover_response}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
#
#    # Retrieve Token from CCF
#    ${scope}=    Create Scope    ${register_user_info_provider['aef_id']}    ${api_name}
#    ${request_body}=    Create Access Token Req Body    ${register_user_info_invoker['api_invoker_id']}    ${scope}
#    ${resp}=    Post Request Capif
#    ...    /capif-security/v1/securities/${API_INVOKER_NOT_VALID}/token
#    ...    data=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${AEF_PROVIDER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    401    AccessTokenErr
#    ...    error=unauthorized_client
#    ...    error_description=Role not authorized for this API route
#
#Retrieve access token with invalid apiInvokerId
#    [Tags]    capif_security_api-22
#    # Default Invoker Registration and Onboarding
#    # Register APF
#    ${register_user_info_provider}=    Provider Default Registration
#    ${api_name}=    Set Variable    service_1
#
#    # Register One Service
#    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
#    ...    ${register_user_info_provider}
#    ...    ${api_name}
#
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    # Test
#    ${discover_response}=    Get Request Capif
#    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${discover_response}    200    DiscoveredAPIs
#
#    # create Security Context
#    ${request_body}=    Create Service Security From Discover Response
#    ...    ${NOTIFICATION_DESTINATION}
#    ...    ${discover_response}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
#
#    # Retrieve Token from CCF
#    ${scope}=    Create Scope    ${register_user_info_provider['aef_id']}    ${api_name}
#    ${request_body}=    Create Access Token Req Body    ${register_user_info_invoker['api_invoker_id']}    ${scope}
#    ${resp}=    Post Request Capif
#    ...    /capif-security/v1/securities/${API_INVOKER_NOT_VALID}/token
#    ...    data=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    404    ProblemDetails29571
#    ...    title=Not Found
#    ...    status=404
#    ...    detail=Security context not found
#    ...    cause=API Invoker has no security context
#
#Retrieve access token with invalid client_id
#    [Tags]    capif_security_api-23
#    # Default Invoker Registration and Onboarding
#    # Register APF
#    ${register_user_info_provider}=    Provider Default Registration
#    ${api_name}=    Set Variable    service_1
#
#    # Register One Service
#    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
#    ...    ${register_user_info_provider}
#    ...    ${api_name}
#
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    # Test
#    ${discover_response}=    Get Request Capif
#    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${discover_response}    200    DiscoveredAPIs
#
#    # create Security Context
#    ${request_body}=    Create Service Security From Discover Response
#    ...    ${NOTIFICATION_DESTINATION}
#    ...    ${discover_response}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
#
#    # Retrieve Token from CCF
#    ${scope}=    Create Scope    ${register_user_info_provider['aef_id']}    ${api_name}
#    ${request_body}=    Create Access Token Req Body    ${API_INVOKER_NOT_VALID}    ${scope}
#    ${resp}=    Post Request Capif
#    ...    /capif-security/v1/securities/${register_user_info_invoker['api_invoker_id']}/token
#    ...    data=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    400    AccessTokenErr
#    ...    error=invalid_client
#    ...    error_description=Client Id not found
#
#Retrieve access token with unsupported grant_type
#    [Tags]    capif_security_api-24
#    # Default Invoker Registration and Onboarding
#    # Register APF
#    ${register_user_info_provider}=    Provider Default Registration
#    ${api_name}=    Set Variable    service_1
#
#    # Register One Service
#    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
#    ...    ${register_user_info_provider}
#    ...    ${api_name}
#
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    # Test
#    ${discover_response}=    Get Request Capif
#    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${discover_response}    200    DiscoveredAPIs
#
#    # create Security Context
#    ${request_body}=    Create Service Security From Discover Response
#    ...    ${NOTIFICATION_DESTINATION}
#    ...    ${discover_response}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
#
#    # Retrieve Token from CCF
#    ${scope}=    Create Scope    ${register_user_info_provider['aef_id']}    ${api_name}
#    ${grant_type}=    Set Variable    not_valid
#    ${request_body}=    Create Access Token Req Body
#    ...    ${register_user_info_invoker['api_invoker_id']}
#    ...    ${scope}
#    ...    grant_type=${grant_type}
#    ${resp}=    Post Request Capif
#    ...    /capif-security/v1/securities/${register_user_info_invoker['api_invoker_id']}/token
#    ...    data=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values
#    ...    ${resp}
#    ...    400
#    ...    AccessTokenErr
#    ...    error=unsupported_grant_type
#    ...    error_description=Invalid value for `grant_type` \\(${grant_type}\\), must be one of \\['client_credentials'\\] - 'grant_type'
#
#Retrieve access token with invalid scope
#    [Tags]    capif_security_api-25
#    # Default Invoker Registration and Onboarding
#    # Register APF
#    ${register_user_info_provider}=    Provider Default Registration
#    ${api_name}=    Set Variable    service_1
#
#    # Register One Service
#    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
#    ...    ${register_user_info_provider}
#    ...    ${api_name}
#
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    # Test
#    ${discover_response}=    Get Request Capif
#    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${discover_response}    200    DiscoveredAPIs
#
#    # create Security Context
#    ${request_body}=    Create Service Security From Discover Response
#    ...    ${NOTIFICATION_DESTINATION}
#    ...    ${discover_response}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
#
#    # Retrieve Token from CCF
#    ${scope}=    Create Scope    ${register_user_info_provider['aef_id']}    ${api_name}
#    ${request_body}=    Create Access Token Req Body
#    ...    ${register_user_info_invoker['api_invoker_id']}
#    ...    "not-valid-scope"
#    ${resp}=    Post Request Capif
#    ...    /capif-security/v1/securities/${register_user_info_invoker['api_invoker_id']}/token
#    ...    data=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    400    AccessTokenErr
#    ...    error=invalid_scope
#    ...    error_description=The first characters must be '3gpp'
#
#Retrieve access token with invalid aefid at scope
#    [Tags]    capif_security_api-26
#    # Default Invoker Registration and Onboarding
#    # Register APF
#    ${register_user_info_provider}=    Provider Default Registration
#    ${api_name}=    Set Variable    service_1
#
#    # Register One Service
#    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
#    ...    ${register_user_info_provider}
#    ...    ${api_name}
#
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    # Test
#    ${discover_response}=    Get Request Capif
#    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${discover_response}    200    DiscoveredAPIs
#
#    # create Security Context
#    ${request_body}=    Create Service Security From Discover Response
#    ...    ${NOTIFICATION_DESTINATION}
#    ...    ${discover_response}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
#
#    # Retrieve Token from CCF
#    ${scope}=    Create Scope    ${register_user_info_provider['aef_id']}    ${api_name}
#    ${request_body}=    Create Access Token Req Body
#    ...    ${register_user_info_invoker['api_invoker_id']}
#    ...    3gpp#1234:${api_name}
#    ${resp}=    Post Request Capif
#    ...    /capif-security/v1/securities/${register_user_info_invoker['api_invoker_id']}/token
#    ...    data=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    400    AccessTokenErr
#    ...    error=invalid_scope
#    ...    error_description=One of aef_id not belongs of your security context
#
#Retrieve access token with invalid apiName at scope
#    [Tags]    capif_security_api-27
#    # Default Invoker Registration and Onboarding
#    # Register APF
#    ${register_user_info_provider}=    Provider Default Registration
#    ${api_name}=    Set Variable    service_1
#
#    # Register One Service
#    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
#    ...    ${register_user_info_provider}
#    ...    ${api_name}
#
#    # Default Invoker Registration and Onboarding
#    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding
#
#    # Test
#    ${discover_response}=    Get Request Capif
#    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${discover_response}    200    DiscoveredAPIs
#
#    # create Security Context
#    ${request_body}=    Create Service Security From Discover Response
#    ...    ${NOTIFICATION_DESTINATION}
#    ...    ${discover_response}
#    ${resp}=    Put Request Capif
#    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['api_invoker_id']}
#    ...    json=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    Check Response Variable Type And Values    ${resp}    201    ServiceSecurity
#
#    # Retrieve Token from CCF
#    ${not_valid_api_name}=    Set Variable    not-valid
#    ${request_body}=    Create Access Token Req Body
#    ...    ${register_user_info_invoker['api_invoker_id']}
#    ...    3gpp#${register_user_info_provider['aef_id']}:${not_valid_api_name}
#    ${resp}=    Post Request Capif
#    ...    /capif-security/v1/securities/${register_user_info_invoker['api_invoker_id']}/token
#    ...    data=${request_body}
#    ...    server=${CAPIF_HTTPS_URL}
#    ...    verify=ca.crt
#    ...    username=${INVOKER_USERNAME}
#
#    # Check Results
#    Check Response Variable Type And Values    ${resp}    400    AccessTokenErr
#    ...    error=invalid_scope
#    ...    error_description=One of the api names does not exist or is not associated with the aef id provided
