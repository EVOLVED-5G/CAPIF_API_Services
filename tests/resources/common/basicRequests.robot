*** Settings ***
Documentation    This resource file contains the basic requests used by Capif. NGINX_HOSTNAME and CAPIF_AUTH can be set as global variables, depends on environment used
Library          RequestsLibrary
Library          Collections

*** Variables ***
${NGINX_HOSTNAME}    http://localhost:8080
${CAPIF_AUTH}
${CAPIF_BEARER}
*** keywords ***
Create CAPIF Session
    [Arguments]    ${server}=${NONE}    ${auth}=${NONE}

    Run Keyword If    "${server}" != "${NONE}"    Create Session    apisession    ${server}            verify=True
    ...               ELSE                        Create Session    apisession    ${NGINX_HOSTNAME}    verify=True

    ${headers}=    Run Keyword If    "${CAPIF_BEARER}" != ""                                   Create Dictionary    Authorization=Bearer ${CAPIF_BEARER}    
    ...            ELSE IF           "${auth}" != "${NONE}"                                    Create Dictionary    Authorization=Basic ${auth}
    ...            ELSE IF           "${CAPIF_AUTH}" != "${NONE}" and "${CAPIF_AUTH}" != ""    Create Dictionary    Authorization=Basic ${CAPIF_AUTH}
    ...            ELSE              Create Dictionary

    [Return]    ${headers}

Post Request Capif
    [Arguments]    ${endpoint}    ${json}=${EMTPY}    ${server}=${NONE}    ${auth}=${NONE}
    [Timeout]      60s

    ${headers}=    Create CAPIF Session    ${server}    ${auth}

    ${resp}=    POST On Session    apisession    ${endpoint}    headers=${headers}    json=${json}    expected_status=any

    [Return]    ${resp}

Post Request Capif Cert
    [Arguments]    ${endpoint}        ${json}=${NONE}    ${server}=${NONE}    ${auth}=${NONE}       ${verify}=${FALSE}    ${data}=${NONE}
    [Timeout]      60s

    ${headers}=    Create CAPIF Session    ${server}    ${auth}

    Set To Dictionary   ${headers}     Content-Type=application/json

    ${resp}=    POST On Session    apisession    ${endpoint}    headers=${headers}    json=${json}    expected_status=any    verify=${verify}   data=${data}

    [Return]    ${resp}


Get Request Capif
    [Arguments]    ${endpoint}    ${server}=${NONE}    ${auth}=${NONE}
    [Timeout]      60s

    ${headers}=    Create CAPIF Session    ${server}    ${auth}

    ${resp}=    GET On Session    apisession    ${endpoint}    headers=${headers}    expected_status=any

    [Return]    ${resp}

Get Request Capif Cert
    [Arguments]    ${endpoint}    ${server}=${NONE}    ${auth}=${NONE}   ${verify}=${FALSE}   ${cert}=${NONE}
    [Timeout]      60s

    # ${headers}=    Create CAPIF Session    ${server}    ${auth}

    Create Session    apisession    ${server}            verify=True

    ${headers}=    Create Dictionary    Content-Type=application/json

    ${resp}=    GET On Session    apisession    ${endpoint}    headers=${headers}    expected_status=any  verify=${verify}   cert=${cert}

    [Return]    ${resp}

Put Request Capif
    [Arguments]    ${endpoint}    ${json}=${EMTPY}    ${server}=${NONE}    ${auth}=${NONE}
    [Timeout]      60s

    ${headers}=    Create CAPIF Session    ${server}    ${auth}

    ${resp}=    PUT On Session    apisession    ${endpoint}    headers=${headers}    json=${json}    expected_status=any
    [Return]    ${resp}


Delete Request Capif
    [Arguments]    ${endpoint}    ${server}=${NONE}    ${auth}=${NONE}
    [Timeout]      60s

    ${headers}=    Create CAPIF Session    ${server}    ${auth}

    ${resp}=    DELETE On Session    apisession    ${endpoint}    headers=${headers}    expected_status=any
    [Return]    ${resp}

Register User At Jwt Auth
    [Arguments]    ${password}=password    ${username}=robot    ${role}=invoker    ${description}=Testing   ${cn}=robot_dummy

    &{body}=    Create Dictionary    password=${password}    username=${username}    role=${role}    description=${description}  cn=${cn}

    Create Session    jwtsession    ${NGINX_HOSTNAME}     verify=True

    ${resp}=    POST On Session    jwtsession    /register    json=${body}

    Should Be Equal As Strings    ${resp.status_code}    201

    Set Global Variable    ${APF_ID}    ${resp.json()['id']}
    ${netappID}=                 Set Variable    ${resp.json()['id']}
    ${ccf_onboarding_url}=     Set Variable    ${resp.json()['ccf_onboarding_url']}
    ${ccf_discover_url}=         Set Variable    ${resp.json()['ccf_discover_url']}

    ${access_token}=    Get Token For User    ${username}    ${password}   ${role}

    [Return]    ${access_token}    ${netappID}   ${ccf_onboarding_url}   ${ccf_discover_url}

Get Token For User
    [Arguments]    ${username}    ${password}   ${role}

    &{body}=    Create Dictionary    username=${username}    password=${password}    role=${role}

    ${resp}=    POST On Session    jwtsession    /gettoken    json=${body}

    Should Be Equal As Strings    ${resp.status_code}    201

    Set Global Variable    ${CAPIF_BEARER}    ${resp.json()["access_token"]}

    [Return]    ${resp.json()["access_token"]}

Clean Test Information By HTTP Requests
    Create Session    jwtsession    ${NGINX_HOSTNAME}     verify=True

    ${resp}=                      DELETE On Session      jwtsession    /testdata
    Should Be Equal As Strings    ${resp.status_code}    200

    ${resp}=                      DELETE On Session      jwtsession    /certdata
    Should Be Equal As Strings    ${resp.status_code}    200

