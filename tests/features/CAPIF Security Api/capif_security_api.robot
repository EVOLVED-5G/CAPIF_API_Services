*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Library     /opt/robot-tests/tests/libraries/bodyRequests.py
Resource    /opt/robot-tests/tests/resources/common/basicRequests.robot

Test Setup    Reset Db

*** Variables ***
${APF_ID_NOT_VALID}            apf-example
${SERVICE_API_ID_NOT_VALID}    not-valid

*** Keywords ***


*** Test Cases ***
Publish API by Authorised API Publisher
	[Tags]    capif_security_api-1
	Log    HELLO WORLD
