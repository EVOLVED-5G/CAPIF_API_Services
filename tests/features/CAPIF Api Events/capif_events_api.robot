*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Library     /opt/robot-tests/tests/libraries/api_events/bodyRequests.py
Resource    /opt/robot-tests/tests/resources/common/basicRequests.robot

Test Setup    Initialize Test And Register    role=invoker

*** Variables ***

*** Keywords ***


*** Test Cases ***
Creates a new individual CAPIF Event Subscription
    [Tags]    capif_api_events-1

    ${request_body}=    Create Events Subscription
    ${resp}=            Post Request Capif            /capif-events/v1/${APF_ID}/subscriptions    ${request_body}

    Should Be Equal As Strings    ${resp.status_code}    201

    ${url}=    Parse Url    ${resp.headers['Location']}

    Should Match Regexp    ${url.path}    ^/capif-events/v1/[0-9a-zA-Z]+/subscriptions/[0-9a-zA-Z]+

Creates a new individual CAPIF Event Subscription with Invalid SubscriberId
    [Tags]    capif_api_events-2

Deletes an individual CAPIF Event Subscription
    [Tags]    capif_api_events-3

Deletes an individual CAPIF Event Subscription with invalid SubscriberId
    [Tags]    capif_api_events-4

Deletes an individual CAPIF Event Subscription with invalid SubscriptionId
    [Tags]    capif_api_events-5
