*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource

Suite Setup     Prepare environment

Force Tags      all

*** Variables ***


*** Keywords ***
Prepare environment
    Add Dns To Hosts    ${CAPIF_IP}    ${CAPIF_HOSTNAME}
    Reset Testing Environment
    # Obtain ca root certificate
    Retrieve Ca Root

Retrieve Ca Root
    [Documentation]    This keyword retrieve ca.root from CAPIF and store it at ca.crt in order to use at TLS communications
    ${resp}=    Get Request Capif    /ca-root   server=http://${CAPIF_HOSTNAME}:8080
    Status Should Be    201    ${resp}
    Log    ${resp.json()['certificate']}
    Store In File    ca.crt    ${resp.json()['certificate']}
