*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Library         /opt/robot-tests/tests/libraries/bodyRequests.py
Library         Collections
Resource        /opt/robot-tests/tests/resources/common/basicRequests.robot
Resource        ../../resources/common.resource

Test Setup      Reset Testing Environment


*** Variables ***
${APF_ID_NOT_VALID}             apf-example
${SERVICE_API_ID_NOT_VALID}     not-valid
${API_INVOKER_NOT_VALID}        not-valid


*** Test Cases ***
Create a security context for an API invoker
    [Tags]    capif_security_api-1
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Create Security Context
    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Results
    Status Should Be    201    ${resp}
    Check Variable    ${resp.json()}    ServiceSecurity
    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_SECURITY_RESOURCE_REGEX}

Create a security context for an API invoker with Provider role
    [Tags]    capif_security_api-2
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Register Provider
    ${register_user_info_publisher}=    Provider Default Registration

    # Create Security Context
    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    # Check Results
    Status Should Be    403    ${resp}
    Check Problem Details    ${resp}
    ...    title=Forbidden
    ...    status=403
    ...    detail=Role not authorized for this API route
    ...    cause=User role must be invoker

Create a security context for an API invoker with Provider entity role and invalid apiInvokerId
    [Tags]    capif_security_api-3
    # Register APF
    ${register_user_info_publisher}=    Provider Default Registration

    # Create Security Context
    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    # Check Results
    Status Should Be    403    ${resp}
    Check Problem Details    ${resp}
    ...    title=Forbidden
    ...    status=403
    ...    detail=Role not authorized for this API route
    ...    cause=User role must be invoker

Create a security context for an API invoker with Invalid apiInvokerID
    [Tags]    capif_security_api-4
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Results
    Status Should Be    404    ${resp}
    Check Problem Details    ${resp}
    ...    title=Not Found
    ...    status=404
    ...    detail=Invoker not found
    ...    cause=API Invoker not exists or invalid ID

Retrieve the Security Context of an API Invoker
    [Tags]    capif_security_api-5
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    201    ${resp}
    Check Variable    ${resp.json()}    ServiceSecurity
    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_SECURITY_RESOURCE_REGEX}

    ${service_security_context}=    Set Variable    ${resp.json()}

    #Register APF
    ${register_user_info_publisher}=    Provider Default Registration

    ${resp}=    Get Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    # Check Results
    Status Should Be    200    ${resp}
    Check Variable    ${resp.json()}    ServiceSecurity
    Dictionaries Should Be Equal    ${resp.json()}    ${service_security_context}

Retrieve the Security Context of an API Invoker with invalid apiInvokerID
    [Tags]    capif_security_api-6
    #Register APF
    ${register_user_info_publisher}=    Provider Default Registration

    ${resp}=    Get Request Capif
    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    Status Should Be    404    ${resp}
    Check Problem Details    ${resp}
    ...    title=Not Found
    ...    status=404
    ...    detail=Invoker not found
    ...    cause=API Invoker not exists or invalid ID

Retrieve the Security Context of an API Invoker with invalid apfId
    [Tags]    capif_security_api-7
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    201    ${resp}

    # We will request information using invoker user, that is not allowed
    ${resp}=    Get Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Results
    Status Should Be    403    ${resp}
    Check Problem Details    ${resp}
    ...    title=Forbidden
    ...    status=403
    ...    detail=Role not authorized for this API route
    ...    cause=User role must be provider

Delete the Security Context of an API Invoker
    [Tags]    capif_security_api-8
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    201    ${resp}

    # Register APF
    ${register_user_info_publisher}=    Provider Default Registration

    # Remove Security Context
    ${resp}=    Delete Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    Status Should Be    204    ${resp}

    # Check if Security Context is removed
    ${resp}=    Get Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    Status Should Be    404    ${resp}
    Check Problem Details    ${resp}
    ...    title=Not Found
    ...    status=404
    ...    detail=Invoker not found
    ...    cause=API Invoker not exists or invalid ID

Delete the Security Context of an API Invoker with Invoker entity role
    [Tags]    capif_security_api-9
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    201    ${resp}

    ${resp}=    Delete Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Result
    Status Should Be    403    ${resp}
    Check Problem Details    ${resp}
    ...    title=Forbidden
    ...    status=403
    ...    detail=Role not authorized for this API route
    ...    cause=User role must be provider

Delete the Security Context of an API Invoker with Invoker entity role and invalid apiInvokerID
    [Tags]    capif_security_api-10
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${resp}=    Delete Request Capif
    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Result
    Status Should Be    403    ${resp}
    Check Problem Details    ${resp}
    ...    title=Forbidden
    ...    status=403
    ...    detail=Role not authorized for this API route
    ...    cause=User role must be provider

Delete the Security Context of an API Invoker with invalid apiInvokerID
    [Tags]    capif_security_api-11
    # Register Provider
    ${register_user_info_publisher}=    Provider Default Registration

    ${resp}=    Delete Request Capif
    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    # Check Result
    Status Should Be    404    ${resp}
    Check Problem Details    ${resp}
    ...    title=Not Found
    ...    status=404
    ...    detail=Invoker not found
    ...    cause=API Invoker not exists or invalid ID

Update the Security Context of an API Invoker
    [Tags]    capif_security_api-12
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Register Provider
    ${register_user_info_publisher}=    Provider Default Registration

    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Results
    Status Should Be    201    ${resp}
    Check Variable    ${resp.json()}    ServiceSecurity

    # Store Initial Security Context
    ${security_context}=    Set Variable    ${resp.json()}

    # Update Security Context
    ${request_body}=    Create Service Security Body    http://robot.testing2
    ${resp}=    Post Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}/update
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    200    ${resp}
    Check Variable    ${resp.json()}    ServiceSecurity

    # Store Security Context modified.
    ${security_context_modified}=    Set Variable    ${resp.json()}

    # Check Security Context is corretly modified at CCF
    ${resp}=    Get Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    # Check Results
    Status Should Be    200    ${resp}
    Check Variable    ${resp.json()}    ServiceSecurity
    Dictionaries Should Be Equal    ${resp.json()}    ${security_context_modified}

Update the Security Context of an API Invoker with Provider entity role
    [Tags]    capif_security_api-13
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    201    ${resp}
    Check Variable    ${resp.json()}    ServiceSecurity

    #Register Provider
    ${register_user_info_publisher}=    Provider Default Registration

    ${resp}=    Post Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}/update
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    # Check Results
    Status Should Be    403    ${resp}
    Check Problem Details    ${resp}
    ...    title=Forbidden
    ...    status=403
    ...    detail=Role not authorized for this API route
    ...    cause=User role must be invoker

Update the Security Context of an API Invoker with AEF entity role and invalid apiInvokerId
    [Tags]    capif_security_api-14
    #Register Provider
    ${register_user_info_publisher}=    Provider Default Registration

    ${request_body}=    Create Service Security Body
    ${resp}=    Post Request Capif
    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}/update
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    Status Should Be    403    ${resp}
    Check Problem Details    ${resp}
    ...    title=Forbidden
    ...    status=403
    ...    detail=Role not authorized for this API route
    ...    cause=User role must be invoker

Update the Security Context of an API Invoker with invalid apiInvokerID
    [Tags]    capif_security_api-15
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Service Security Body
    ${resp}=    Post Request Capif
    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}/update
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Result
    Status Should Be    404    ${resp}
    Check Problem Details    ${resp}
    ...    title=Not Found
    ...    status=404
    ...    detail=Invoker not found
    ...    cause=API Invoker not exists or invalid ID

Revoke the authorization of the API invoker for APIs
    [Tags]    capif_security_api-16
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    201    ${resp}
    Check Variable    ${resp.json()}    ServiceSecurity

    # Register Provider
    ${register_user_info_publisher}=    Provider Default Registration

    ${request_body}=    Create Security Notification Body    ${register_user_info_invoker['apiInvokerId']}
    ${resp}=    Post Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}/delete
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    # Check Results
    Status Should Be    204    ${resp}

    # Check if Security Context is removed
    ${resp}=    Get Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    Status Should Be    404    ${resp}
    Check Problem Details    ${resp}
    ...    title=Not Found
    ...    status=404
    ...    detail=Invoker not found
    ...    cause=API Invoker not exists or invalid ID

Revoke the authorization of the API invoker for APIs without valid apfID.
    [Tags]    capif_security_api-17
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    201    ${resp}
    Check Variable    ${resp.json()}    ServiceSecurity

    ${security_context}=    Set Variable    ${resp.json()}

    # Register Provider
    ${register_user_info_publisher}=    Provider Default Registration

    # Revoke Security Context by Invoker
    ${request_body}=    Create Security Notification Body    ${register_user_info_invoker['apiInvokerId']}
    ${resp}=    Post Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}/delete
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Results
    Status Should Be    403    ${resp}
    Check Problem Details    ${resp}
    ...    title=Forbidden
    ...    status=403
    ...    detail=Role not authorized for this API route
    ...    cause=User role must be provider

    ${resp}=    Get Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    # Check Results
    Status Should Be    200    ${resp}
    Check Variable    ${resp.json()}    ServiceSecurity
    Dictionaries Should Be Equal    ${resp.json()}    ${security_context}

Revoke the authorization of the API invoker for APIs with invalid apiInvokerId
    [Tags]    capif_security_api-18
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    201    ${resp}
    Check Variable    ${resp.json()}    ServiceSecurity

    ${security_context}=    Set Variable    ${resp.json()}

    #Register Provider
    ${register_user_info_publisher}=    Provider Default Registration

    ${request_body}=    Create Security Notification Body    ${API_INVOKER_NOT_VALID}
    ${resp}=    Post Request Capif
    ...    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}/delete
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    # Check Results
    Status Should Be    404    ${resp}
    Check Problem Details    ${resp}
    ...    title=Not Found
    ...    status=404
    ...    detail=Invoker not found
    ...    cause=API Invoker not exists or invalid ID

    ${resp}=    Get Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    # Check Results
    Status Should Be    200    ${resp}
    Check Variable    ${resp.json()}    ServiceSecurity
    Dictionaries Should Be Equal    ${resp.json()}    ${security_context}

Retrieve access token
    [Tags]    capif_security_api-19
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    201    ${resp}

    # Retrieve Token from CCF
    ${request_body}=    Create Access Token Req Body
    ${resp}=    Post Request Capif
    ...    /capif-security/v1/securities/${register_user_info_invoker['apiInvokerId']}/token
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    200    AccessTokenRsp
    ...    token_type=Bearer

    Should Not Be Empty    ${resp.json()['access_token']}

Retrieve access token by Provider
    [Tags]    capif_security_api-20
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Service Security Body
    ${resp}=    Put Request Capif
    ...    /capif-security/v1/trustedInvokers/${register_user_info_invoker['apiInvokerId']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    201    ${resp}

    #Register Provider
    ${register_user_info_publisher}=    Provider Default Registration

    ${request_body}=    Create Access Token Req Body
    ${resp}=    Post Request Capif
    ...    /capif-security/v1/securities/${register_user_info_invoker['apiInvokerId']}/token
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    400    AccessTokenErr
    ...    error=invalid_client
    ...    error_description=Role not authorized for this API route

Retrieve access token by Provider with invalid apiInvokerId
    [Tags]    capif_security_api-21
    #Register APF
    ${register_user_info_publisher}=    Provider Default Registration

    ${request_body}=    Create Access Token Req Body
    ${resp}=    Post Request Capif
    ...    /capif-security/v1/securities/${API_INVOKER_NOT_VALID}/token
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PROVIDER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    400    AccessTokenErr
    ...    error=invalid_client
    ...    error_description=Role not authorized for this API route

Retrieve access token with invalid apiInvokerId
    [Tags]    capif_security_api-22
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Access Token Req Body
    ${resp}=    Post Request Capif
    ...    /capif-security/v1/securities/${API_INVOKER_NOT_VALID}/token
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check Results
    Check Response Variable Type And Values    ${resp}    400    AccessTokenErr
    ...    error=invalid_request
    ...    error_description=No Security Context for this API Invoker
