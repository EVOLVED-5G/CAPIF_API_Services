*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Library     /opt/robot-tests/tests/libraries/api_events/bodyRequests.py
Resource    /opt/robot-tests/tests/resources/common/basicRequests.robot

Test Setup    Initialize Test And Register    role=apf    db_col=serviceapidescriptions

*** Variables ***

*** Keywords ***


*** Test Cases ***
