*** Settings ***
Documentation       This resource file contains the basic requests used by Capif. NGINX_HOSTNAME and CAPIF_AUTH can be set as global variables, depends on environment used

Library             RequestsLibrary
Library             Collections


*** Variables ***
${NGINX_HOSTNAME}       http://localhost:8080
${CAPIF_AUTH}
${CAPIF_BEARER}


*** Keywords ***
Create CAPIF Session
    [Arguments]    ${server}=${NONE}    ${auth}=${NONE}

    IF    "${server}" != "${NONE}"
        Create Session    apisession    ${server}    verify=True
    ELSE
        Create Session    apisession    ${NGINX_HOSTNAME}    verify=True
    END

    IF    "${CAPIF_BEARER}" != ""
        ${headers}=    Create Dictionary    Authorization=Bearer ${CAPIF_BEARER}
    ELSE IF    "${auth}" != "${NONE}"
        ${headers}=    Create Dictionary    Authorization=Basic ${auth}
    ELSE IF    "${CAPIF_AUTH}" != "${NONE}" and "${CAPIF_AUTH}" != ""
        ${headers}=    Create Dictionary    Authorization=Basic ${CAPIF_AUTH}
    ELSE
        ${headers}=    Create Dictionary
    END
    RETURN    ${headers}


Post Request Capif
    [Timeout]    60s
    [Arguments]    ${endpoint}    ${json}=${NONE}    ${server}=${NONE}    ${auth}=${NONE}    ${verify}=${FALSE}    ${data}=${NONE}

    ${headers}=    Create CAPIF Session    ${server}    ${auth}

    Set To Dictionary    ${headers}    Content-Type=application/json

    ${resp}=    POST On Session
    ...    apisession
    ...    ${endpoint}
    ...    headers=${headers}
    ...    json=${json}
    ...    expected_status=any
    ...    verify=${verify}
    ...    data=${data}
    RETURN    ${resp}


Get Request Capif
    [Timeout]    60s
    [Arguments]    ${endpoint}    ${server}=${NONE}    ${auth}=${NONE}    ${verify}=${FALSE}    ${cert}=${NONE}

    ${headers}=    Create CAPIF Session    ${server}    ${auth}

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
    [Arguments]    ${endpoint}    ${json}=${EMTPY}    ${server}=${NONE}    ${auth}=${NONE}

    ${headers}=    Create CAPIF Session    ${server}    ${auth}

    ${resp}=    PUT On Session
    ...    apisession
    ...    ${endpoint}
    ...    headers=${headers}
    ...    json=${json}
    ...    expected_status=any
    RETURN    ${resp}

Delete Request Capif
    [Timeout]    60s
    [Arguments]    ${endpoint}    ${server}=${NONE}    ${auth}=${NONE}

    ${headers}=    Create CAPIF Session    ${server}    ${auth}

    ${resp}=    DELETE On Session    apisession    ${endpoint}    headers=${headers}    expected_status=any
    RETURN    ${resp}

Register User At Jwt Auth
    [Arguments]    ${password}=password    ${username}=robot    ${role}=invoker    ${description}=Testing
    
    # Create certificate and private_key for this machine.
    ${csr_request}=    Create Csr    ${username}.csr    ${username}.key    ${username}

    &{body}=    Create Dictionary
    ...    password=${password}
    ...    username=${username}
    ...    role=${role}
    ...    description=${description}
    ...    cn=${username}

    Create Session    jwtsession    ${NGINX_HOSTNAME}    verify=True

    ${resp}=    POST On Session    jwtsession    /register    json=${body}

    Should Be Equal As Strings    ${resp.status_code}    201

    Set Global Variable    ${APF_ID}    ${resp.json()['id']}
    ${netappID}=    Set Variable    ${resp.json()['id']}
    ${ccf_onboarding_url}=    Set Variable    ${resp.json()['ccf_onboarding_url']}
    ${ccf_discover_url}=    Set Variable    ${resp.json()['ccf_discover_url']}

    ${access_token}=    Get Token For User    ${username}    ${password}    ${role}
    RETURN    ${access_token}    ${netappID}    ${ccf_onboarding_url}    ${ccf_discover_url}   ${csr_request}


Get Token For User
    [Arguments]    ${username}    ${password}    ${role}

    &{body}=    Create Dictionary    username=${username}    password=${password}    role=${role}

    ${resp}=    POST On Session    jwtsession    /gettoken    json=${body}

    Should Be Equal As Strings    ${resp.status_code}    201

    Set Global Variable    ${CAPIF_BEARER}    ${resp.json()["access_token"]}
    RETURN    ${resp.json()["access_token"]}


Clean Test Information By HTTP Requests
    Create Session    jwtsession    ${NGINX_HOSTNAME}    verify=True

    ${resp}=    DELETE On Session    jwtsession    /testdata
    Should Be Equal As Strings    ${resp.status_code}    200

    ${resp}=    DELETE On Session    jwtsession    /certdata
    Should Be Equal As Strings    ${resp.status_code}    200
