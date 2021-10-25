*** Settings ***
Documentation    This resource file contains the basic requests used by Capif. CAPIF_SERVER and CAPIF_AUTH can be set as global variables, depends on environment used
Library          RequestsLibrary
Library          Collections

*** Variables ***
${CAPIF_SERVER}
${CAPIF_AUTH}

*** keywords ***
Create CAPIF Session
    [Arguments]    ${server}=${NONE}    ${auth}=${NONE}

    Run Keyword If    "${server}" != "${NONE}"    Create Session    apisession    ${server}    verify=True
    ...               ELSE                        Create Session    apisession    ${CAPIF_SERVER}    verify=True

    ${headers}=    Run Keyword If    "${auth}" != "${NONE}"    Create Dictionary    Authorization=Basic ${auth}
    ...            ELSE IF           "${CAPIF_AUTH}" != "${NONE}" and "${CAPIF_AUTH}" != ""    Create Dictionary    Authorization=Basic ${CAPIF_AUTH}
    ...            ELSE              Create Dictionary

    [Return]    ${headers}

Post Request Capif
    [Arguments]    ${endpoint}    ${json}=${EMTPY}    ${server}=${NONE}    ${auth}=${NONE}
    [Timeout]      60s

    ${headers}=    Create CAPIF Session    ${server}  ${auth}

    ${resp}=    POST On Session    apisession    ${endpoint}    headers=${headers}    json=${json}

    [Return]    ${resp}

Get Request Capif
    [Arguments]    ${endpoint}   ${server}=${NONE}    ${auth}=${NONE}
    [Timeout]      60s

    ${headers}=    Create CAPIF Session    ${server}  ${auth}

    ${resp}=    GET On Session    apisession    ${endpoint}    

    [Return]    ${resp}

Put Request Capif
    [Arguments]    ${endpoint}    ${json}=${EMTPY}   ${server}=${NONE}    ${auth}=${NONE}
    [Timeout]      60s

    ${headers}=    Create CAPIF Session    ${server}  ${auth}

    ${resp}=    PUT On Session    apisession    ${endpoint}    headers=${headers}    json=${json}
    [Return]    ${resp}


Delete Request Capif
    [Arguments]    ${endpoint}   ${server}=${NONE}    ${auth}=${NONE}
    [Timeout]      60s

    ${headers}=    Create CAPIF Session    ${server}  ${auth}

    ${resp}=    DELETE On Session    apisession    ${endpoint}    headers=${headers}
    [Return]    ${resp}

