*** Settings ***
Library     /opt/robot-tests/tests/libraries/helpers.py
Resource    /opt/robot-tests/tests/resources/common/basicRequests.robot


*** Variables ***
${INVOKER_USERNAME}             ROBOT_TESTING_INVOKER
${PUBLISHER_USERNAME}           ROBOT_TESTING_PUBLISHER
${INVOKER_NOT_REGISTERED}       not-valid
${INVOKER_ROLE}                 invoker
${PUBLISHER_ROLE}                apf

${CAPIF_HOSTNAME}               capifcore
${CAPIF_CALLBACK_IP}            host.docker.internal
${CAPIF_CALLBACK_PORT}          8086


*** Keywords ***
Reset Testing Environment
    Log    Db capif.invokerdetails collection will be removed in order to isolate each test.

    Clean Test Information By HTTP Requests
