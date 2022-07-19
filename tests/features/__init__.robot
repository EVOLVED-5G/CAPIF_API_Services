*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource

Suite Setup     Prepare environment

Force Tags      all


*** Variables ***


*** Keywords ***
Prepare environment
    Log    ${CAPIF_HOSTNAME}
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
    ${resp}=    Get Request Capif    /ca-root    server=http://${CAPIF_HOSTNAME}
    Status Should Be    201    ${resp}
    Log    ${resp.json()['certificate']}
    Store In File    ca.crt    ${resp.json()['certificate']}
