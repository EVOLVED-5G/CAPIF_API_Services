*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Library     /opt/robot-tests/tests/libraries/api_events/bodyRequests.py
Resource    /opt/robot-tests/tests/resources/common/basicRequests.robot

Test Setup    Initialize Test And Register    role=invoker

*** Variables ***
${API_INVOKER_NOT_REGISTERED}    not-valid
${SUBSCRIBER_ID_NOT_VALID}       not-valid
${SUBSCRIPTION_ID_NOT_VALID}     not-valid

*** Keywords ***


*** Test Cases ***
Creates a new individual CAPIF Event Subscription
    [Tags]    capif_api_events-1

    ${request_body}=    Create Events Subscription
    ${resp}=            Post Request Capif            /capif-events/v1/${APF_ID}/subscriptions    ${request_body}

    Should Be Equal As Strings    ${resp.status_code}    201

    ${url}=    Parse Url      ${resp.headers['Location']}
    Log        ${url.path}

    Should Match Regexp    ${url.path}    ^/capif-events/v1/[0-9a-zA-Z]+/subscriptions/[0-9a-zA-Z]+

    ${subscriber_id}    ${subscription_id}=    Get Subscriber And Subscription From Location    ${url.path}

Creates a new individual CAPIF Event Subscription with Invalid SubscriberId
    [Tags]    capif_api_events-2

    ${request_body}=    Create Events Subscription
    ${resp}=            Post Request Capif            /capif-events/v1/${API_INVOKER_NOT_REGISTERED}/subscriptions    ${request_body}

    Should Be Equal As Strings    ${resp.status_code}    403


Deletes an individual CAPIF Event Subscription
    [Tags]    capif_api_events-3

    ${subscriber_id}=    Set Variable    ${APF_ID}

    ${request_body}=    Create Events Subscription
    ${resp}=            Post Request Capif            /capif-events/v1/${subscriber_id}/subscriptions    ${request_body}

    Should Be Equal As Strings    ${resp.status_code}    201

    ${url}=             Parse Url              ${resp.headers['Location']}
    ${subscriber_id}    ${subscription_id}=    Get Subscriber And Subscription From Location    ${url.path}

    ${resp}=    Delete Request Capif    /capif-events/v1/${subscriber_id}/subscriptions/${subscription_id}

    Should Be Equal As Strings    ${resp.status_code}    204



Deletes an individual CAPIF Event Subscription with invalid SubscriberId
    [Tags]    capif_api_events-4

    ${subscriber_id}=    Set Variable    ${APF_ID}

    ${request_body}=    Create Events Subscription
    ${resp}=            Post Request Capif            /capif-events/v1/${subscriber_id}/subscriptions    ${request_body}

    Should Be Equal As Strings    ${resp.status_code}    201

    ${url}=             Parse Url              ${resp.headers['Location']}
    ${subscriber_id}    ${subscription_id}=    Get Subscriber And Subscription From Location    ${url.path}

    ${resp}=    Delete Request Capif    /capif-events/v1/${SUBSCRIBER_ID_NOT_VALID}/subscriptions/${subscription_id}

    Should Be Equal As Strings    ${resp.status_code}    403

Deletes an individual CAPIF Event Subscription with invalid SubscriptionId
    [Tags]    capif_api_events-5

    ${subscriber_id}=    Set Variable    ${APF_ID}

    ${request_body}=    Create Events Subscription
    ${resp}=            Post Request Capif            /capif-events/v1/${subscriber_id}/subscriptions    ${request_body}

    Should Be Equal As Strings    ${resp.status_code}    201

    ${url}=             Parse Url              ${resp.headers['Location']}
    ${subscriber_id}    ${subscription_id}=    Get Subscriber And Subscription From Location    ${url.path}

    ${resp}=    Delete Request Capif    /capif-events/v1/${subscriber_id}/subscriptions/${SUBSCRIPTION_ID_NOT_VALID}

    Should Be Equal As Strings    ${resp.status_code}    404
