*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Resource    ../resources/common.resource

Suite Setup     Prepare environment
# Suite Teardown  Reset Testing Environment

Force Tags      all


*** Keywords ***
Prepare environment
    Log    ${CAPIF_HOSTNAME}
    Log    "${CAPIF_HTTP_PORT}"
    Log    "${CAPIF_HTTPS_PORT}"

    Set Global Variable    ${CAPIF_HTTP_URL}    http://${CAPIF_HOSTNAME}/
    IF    "${CAPIF_HTTP_PORT}" != ""
        Set Global Variable    ${CAPIF_HTTP_URL}    http://${CAPIF_HOSTNAME}:${CAPIF_HTTP_PORT}/
    END

    Set Global Variable    ${CAPIF_HTTPS_URL}    https://${CAPIF_HOSTNAME}/
    IF    "${CAPIF_HTTPS_PORT}" != ""
        Set Global Variable    ${CAPIF_HTTPS_URL}    https://${CAPIF_HOSTNAME}:${CAPIF_HTTPS_PORT}/
    END

    ${status}    ${CAPIF_IP}=    Run Keyword And Ignore Error    Get Ip From Hostname    ${CAPIF_HOSTNAME}

    IF    "${status}" == "PASS"
        Log    We will use a remote deployment
        Log    ${CAPIF_IP}
    ELSE
        Log    We will use a local deployment
        Add Dns To Hosts    127.0.0.1    ${CAPIF_HOSTNAME}
    END
    # Obtain ca root certificate
    Retrieve Ca Root

    Reset Testing Environment

Retrieve Ca Root
    [Documentation]    This keyword retrieve ca.root from CAPIF and store it at ca.crt in order to use at TLS communications
    ${resp}=    Get Request Capif    /ca-root    server=${CAPIF_HTTP_URL}
    Status Should Be    201    ${resp}
    Log    ${resp.json()['certificate']}
    Store In File    ca.crt    ${resp.json()['certificate']}
