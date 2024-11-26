*** Settings ***
Documentation       This resource file contains the basic requests used by Capif. NGINX_HOSTNAME and CAPIF_AUTH can be set as global variables, depends on environment used

Library             RequestsLibrary
Library             Collections
Library             OperatingSystem
Library             XML


*** Variables ***
${CAPIF_AUTH}
${CAPIF_BEARER}

${LOCATION_INVOKER_RESOURCE_REGEX}
...                                     ^/api-invoker-management/v1/onboardedInvokers/[0-9a-zA-Z]+
${LOCATION_EVENT_RESOURCE_REGEX}
...                                     ^/capif-events/v1/[0-9a-zA-Z]+/subscriptions/[0-9a-zA-Z]+
${LOCATION_INVOKER_RESOURCE_REGEX}
...                                     ^/api-invoker-management/v1/onboardedInvokers/[0-9a-zA-Z]+
${LOCATION_PUBLISH_RESOURCE_REGEX}
...                                     ^/published-apis/v1/[0-9a-zA-Z]+/service-apis/[0-9a-zA-Z]+
${LOCATION_SECURITY_RESOURCE_REGEX}
...                                     ^/capif-security/v1/trustedInvokers/[0-9a-zA-Z]+
${LOCATION_PROVIDER_RESOURCE_REGEX}
...                                     ^/api-provider-management/v1/registrations/[0-9a-zA-Z]+
${LOCATION_LOGGING_RESOURCE_REGEX}
...                                     ^/api-invocation-logs/v1/[0-9a-zA-Z]+/logs/[0-9a-zA-Z]+

${INVOKER_ROLE}                         invoker
${AMF_ROLE}                             amf
${APF_ROLE}                             apf
${AEF_ROLE}                             aef


*** Keywords ***
Create CAPIF Session
    [Documentation]    Create needed session and headers.
    ...    If server input data is set to NONE, it will try to use NGINX_HOSTNAME variable.
    [Arguments]    ${server}=${NONE}    ${access_token}=${NONE}    ${verify}=${NONE}

    IF    "${server}" != "${NONE}"
        Create Session    apisession    ${server}    verify=${verify}
    END

    ${headers}=    Create Dictionary
    IF    "${access_token}" != "${NONE}"
        ${headers}=    Create Dictionary    Authorization=Bearer ${access_token}
    END

    RETURN    ${headers}

Post Request Capif
    [Timeout]    60s
    [Arguments]    ${endpoint}    ${json}=${NONE}    ${server}=${NONE}    ${access_token}=${NONE}    ${auth}=${NONE}    ${verify}=${FALSE}    ${cert}=${NONE}    ${username}=${NONE}    ${data}=${NONE}

    ${headers}=    Create CAPIF Session    ${server}    ${access_token}    ${verify}

    IF    '${username}' != '${NONE}'
        ${cert}=    Set variable    ${{ ('${username}.crt','${username}.key') }}
    END

    ${resp}=    POST On Session
    ...    apisession
    ...    ${endpoint}
    ...    headers=${headers}
    ...    json=${json}
    ...    expected_status=any
    ...    verify=${verify}
    ...    cert=${cert}
    ...    data=${data}
    RETURN    ${resp}

Get Request Capif
    [Timeout]    60s
    [Arguments]    ${endpoint}    ${server}=${NONE}    ${access_token}=${NONE}    ${auth}=${NONE}    ${verify}=${FALSE}    ${cert}=${NONE}    ${username}=${NONE}

    ${headers}=    Create CAPIF Session    ${server}    ${access_token}

    IF    '${username}' != '${NONE}'
        ${cert}=    Set variable    ${{ ('${username}.crt','${username}.key') }}
    END

    ${resp}=    GET On Session
    ...    apisession
    ...    ${endpoint}
    ...    headers=${headers}
    ...    expected_status=any
    ...    verify=${verify}
    ...    cert=${cert}
    RETURN    ${resp}

Put Request Capif
    [Timeout]    60s
    [Arguments]    ${endpoint}    ${json}=${NONE}    ${server}=${NONE}    ${access_token}=${NONE}    ${auth}=${NONE}    ${verify}=${FALSE}    ${cert}=${NONE}    ${username}=${NONE}

    ${headers}=    Create CAPIF Session    ${server}    ${access_token}

    IF    '${username}' != '${NONE}'
        ${cert}=    Set variable    ${{ ('${username}.crt','${username}.key') }}
    END

    ${resp}=    PUT On Session
    ...    apisession
    ...    ${endpoint}
    ...    headers=${headers}
    ...    json=${json}
    ...    expected_status=any
    ...    verify=${verify}
    ...    cert=${cert}

    RETURN    ${resp}

Patch Request Capif
    [Timeout]    60s
    [Arguments]    ${endpoint}    ${json}=${NONE}    ${server}=${NONE}    ${access_token}=${NONE}    ${auth}=${NONE}    ${verify}=${FALSE}    ${cert}=${NONE}    ${username}=${NONE}

    ${headers}=    Create CAPIF Session    ${server}    ${access_token}

    IF    '${username}' != '${NONE}'
        ${cert}=    Set variable    ${{ ('${username}.crt','${username}.key') }}
    END

    ${resp}=    PATCH On Session
    ...    apisession
    ...    ${endpoint}
    ...    headers=${headers}
    ...    json=${json}
    ...    expected_status=any
    ...    verify=${verify}
    ...    cert=${cert}

    RETURN    ${resp}

Delete Request Capif
    [Timeout]    60s
    [Arguments]    ${endpoint}    ${server}=${NONE}    ${access_token}=${NONE}    ${auth}=${NONE}    ${verify}=${FALSE}    ${cert}=${NONE}    ${username}=${NONE}

    ${headers}=    Create CAPIF Session    ${server}    ${access_token}

    IF    '${username}' != '${NONE}'
        ${cert}=    Set variable    ${{ ('${username}.crt','${username}.key') }}
    END

    ${resp}=    DELETE On Session
    ...    apisession
    ...    ${endpoint}
    ...    headers=${headers}
    ...    expected_status=any
    ...    verify=${verify}
    ...    cert=${cert}

    RETURN    ${resp}

Register User At Jwt Auth
    [Arguments]    ${username}    ${role}    ${password}=password    ${description}=Testing

    ${cn}=    Set Variable    ${username}
    # Create certificate and private_key for this machine.
    IF    "${role}" == "${INVOKER_ROLE}"
        ${cn}=    Set Variable    invoker
        ${csr_request}=    Create User Csr    ${username}    ${cn}
        Log    inside if cn=${cn}
    ELSE
        ${csr_request}=    Set Variable    ${None}
    END

    Log    cn=${cn}

    &{body}=    Create Dictionary
    ...    password=${password}
    ...    username=${username}
    ...    role=${role}
    ...    description=${description}
    ...    cn=${cn}

    Create Session    jwtsession    ${CAPIF_HTTP_URL}    verify=True

    ${resp}=    POST On Session    jwtsession    /register    json=${body}

    Should Be Equal As Strings    ${resp.status_code}    201

    ${get_auth_response}=    Get Auth For User    ${username}    ${password}

    ${register_user_info}=    Create Dictionary
    ...    netappID=${resp.json()['id']}
    ...    csr_request=${csr_request}
    ...    &{resp.json()}
    ...    &{get_auth_response}

    Log Dictionary    ${register_user_info}

    IF    "ca_root" in @{register_user_info.keys()}
        Store In File    ca.crt    ${register_user_info['ca_root']}
    END

    IF    "cert" in @{register_user_info.keys()}
        Store In File    ${username}.crt    ${register_user_info['cert']}
    END
    IF    "private_key" in @{register_user_info.keys()}
        Store In File    ${username}.key    ${register_user_info['private_key']}
    END

    RETURN    ${register_user_info}

Register User At Jwt Auth Provider
    [Arguments]    ${username}    ${role}    ${password}=password    ${description}=Testing

    ${apf_username}=    Set Variable    APF_${username}
    ${aef_username}=    Set Variable    AEF_${username}
    ${amf_username}=    Set Variable    AMF_${username}

    # Create a certificate for each kind of role under provider
    ${csr_request}=    Create User Csr    ${username}    provider

    ${apf_csr_request}=    Create User Csr    ${apf_username}    apf
    ${aef_csr_request}=    Create User Csr    ${aef_username}    aef
    ${amf_csr_request}=    Create User Csr    ${amf_username}    amf

    # Register provider
    &{body}=    Create Dictionary
    ...    password=${password}
    ...    username=${username}
    ...    role=${role}
    ...    description=${description}
    ...    cn=${username}

    Create Session    jwtsession    ${CAPIF_HTTP_URL}    verify=True

    ${resp}=    POST On Session    jwtsession    /register    json=${body}

    Should Be Equal As Strings    ${resp.status_code}    201

    # Get Auth to obtain access_token
    ${get_auth_response}=    Get Auth For User    ${username}    ${password}

    ${register_user_info}=    Create Dictionary
    ...    netappID=${resp.json()['id']}
    ...    csr_request=${csr_request}
    ...    apf_csr_request=${apf_csr_request}
    ...    aef_csr_request=${aef_csr_request}
    ...    amf_csr_request=${amf_csr_request}
    ...    apf_username=${apf_username}
    ...    aef_username=${aef_username}
    ...    amf_username=${amf_username}
    ...    &{resp.json()}
    ...    &{get_auth_response}

    Log Dictionary    ${register_user_info}

    RETURN    ${register_user_info}

Get Auth For User
    [Arguments]    ${username}    ${password}

    &{body}=    Create Dictionary    username=${username}    password=${password}

    ${resp}=    POST On Session    jwtsession    /getauth    json=${body}

    Should Be Equal As Strings    ${resp.status_code}    200

    # Should Be Equal As Strings    ${resp.json()['message']}    Certificate created successfuly

    RETURN    ${resp.json()}

Clean Test Information By HTTP Requests
    Create Session    jwtsession    ${CAPIF_HTTP_URL}    verify=True

    ${resp}=    DELETE On Session    jwtsession    /testdata
    Should Be Equal As Strings    ${resp.status_code}    200

Invoker Default Onboarding
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

    Set To Dictionary    ${register_user_info}    api_invoker_id=${resp.json()['apiInvokerId']}
    Log Dictionary    ${register_user_info}

    # Assertions
    Status Should Be    201    ${resp}
    Check Variable    ${resp.json()}    APIInvokerEnrolmentDetails
    Check Location Header    ${resp}    ${LOCATION_INVOKER_RESOURCE_REGEX}
    # Store dummy signede certificate
    Store In File    ${INVOKER_USERNAME}.crt    ${resp.json()['onboardingInformation']['apiInvokerCertificate']}

    ${url}=    Parse Url    ${resp.headers['Location']}

    RETURN    ${register_user_info}    ${url}    ${request_body}

Provider Registration
    [Arguments]    ${register_user_info}

    # Create provider Registration Body
    ${apf_func_details}=    Create Api Provider Function Details
    ...    ${register_user_info['apf_username']}
    ...    ${register_user_info['apf_csr_request']}
    ...    APF
    ${aef_func_details}=    Create Api Provider Function Details
    ...    ${register_user_info['aef_username']}
    ...    ${register_user_info['aef_csr_request']}
    ...    AEF
    ${amf_func_details}=    Create Api Provider Function Details
    ...    ${register_user_info['amf_username']}
    ...    ${register_user_info['amf_csr_request']}
    ...    AMF
    ${api_prov_funcs}=    Create List    ${apf_func_details}    ${aef_func_details}    ${amf_func_details}

    ${request_body}=    Create Api Provider Enrolment Details Body
    ...    ${register_user_info['access_token']}
    ...    ${api_prov_funcs}

    # Register Provider
    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    access_token=${register_user_info['access_token']}

    # Check Results
    Check Response Variable Type And Values    ${resp}    201    APIProviderEnrolmentDetails
    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_PROVIDER_RESOURCE_REGEX}

    Log Dictionary    ${resp.json()}

    FOR    ${prov}    IN    @{resp.json()['apiProvFuncs']}
        Log Dictionary    ${prov}
        Store In File    ${prov['apiProvFuncInfo']}.crt    ${prov['regInfo']['apiProvCert']}
        IF    "${prov['apiProvFuncRole']}" == "APF"
            Set To Dictionary    ${register_user_info}    apf_id=${prov['apiProvFuncId']}
        ELSE IF    "${prov['apiProvFuncRole']}" == "AEF"
            Set To Dictionary    ${register_user_info}    aef_id=${prov['apiProvFuncId']}
        ELSE IF    "${prov['apiProvFuncRole']}" == "AMF"
            Set To Dictionary    ${register_user_info}    amf_id=${prov['apiProvFuncId']}
        ELSE
            Fail    "${prov['apiProvFuncRole']} is not valid role"
        END
    END

    Set To Dictionary
    ...    ${register_user_info}
    ...    provider_enrollment_details=${request_body}
    ...    resource_url=${resource_url}
    ...    provider_register_response=${resp}

    RETURN    ${register_user_info}

Provider Default Registration
    #Register Provider
    ${register_user_info}=    Register User At Jwt Auth Provider
    ...    username=${PROVIDER_USERNAME}    role=${PROVIDER_ROLE}

    ${register_user_info}=    Provider Registration    ${register_user_info}

    Log Dictionary    ${register_user_info}
    RETURN    ${register_user_info}

Publish Service Api
    [Arguments]    ${register_user_info_provider}    ${service_name}=service_1

    ${request_body}=    Create Service Api Description    ${service_name}    ${register_user_info_provider['aef_id']}
    ${resp}=    Post Request Capif
    ...    /published-apis/v1/${register_user_info_provider['apf_id']}/service-apis
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${register_user_info_provider['apf_username']}

    Check Response Variable Type And Values    ${resp}    201    ServiceAPIDescription
    Dictionary Should Contain Key    ${resp.json()}    apiId
    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_PUBLISH_RESOURCE_REGEX}

    RETURN    ${resp.json()}    ${resource_url}    ${request_body}
