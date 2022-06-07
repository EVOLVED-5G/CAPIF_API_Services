*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource

Suite Setup     Prepare environment

Force Tags      all


*** Keywords ***
Prepare environment
    Add Dns To Hosts    127.0.0.1    capifcore
    Reset Testing Environment
    # Obtain ca root certificate
    Retrieve Ca Root

Retrieve Ca Root
    [Documentation]    This keyword retrieve ca.root from CAPIF and store it at ca.crt in order to use at TLS communications
    ${resp}=    Get Request Capif    /ca-root
    Status Should Be    201    ${resp}
    Log    ${resp.json()['certificate']}
    Store In File    ca.crt    ${resp.json()['certificate']}
