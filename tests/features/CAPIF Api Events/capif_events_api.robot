*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Library         /opt/robot-tests/tests/libraries/bodyRequests.py
Library         XML
Resource        /opt/robot-tests/tests/resources/common/basicRequests.robot
Resource        ../../resources/common.resource

Test Setup      Reset Testing Environment


*** Variables ***
${API_INVOKER_NOT_REGISTERED}       not-valid
${SUBSCRIBER_ID_NOT_VALID}          not-valid
${SUBSCRIPTION_ID_NOT_VALID}        not-valid


*** Test Cases ***
Creates a new individual CAPIF Event Subscription
    [Tags]    capif_api_events-1
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Events Subscription
    ${resp}=    Post Request Capif
    ...    /capif-events/v1/${register_user_info_invoker['id']}/subscriptions
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Assertions
    Status Should Be    201    ${resp}
    Check Variable    ${resp.json()}    EventSubscription
    ${subscriber_id}    ${subscription_id}=    Check Event Location Header    ${resp}

Creates a new individual CAPIF Event Subscription with Invalid SubscriberId
    [Tags]    capif_api_events-2
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Events Subscription
    ${resp}=    Post Request Capif
    ...    /capif-events/v1/${SUBSCRIBER_ID_NOT_VALID}/subscriptions
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Assertions
    Status Should Be    403    ${resp}
    Check Variable    ${resp.json()}    ProblemDetails
    Check Problem Details     ${resp}   status=403   detail=Event API not existing   cause=Event Subscriptions are not stored in CAPIF Database

Deletes an individual CAPIF Event Subscription
    [Tags]    capif_api_events-3
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Events Subscription
    ${resp}=    Post Request Capif
    ...    /capif-events/v1/${register_user_info_invoker['id']}/subscriptions
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    201    ${resp}
    Check Variable    ${resp.json()}    EventSubscription

    ${subscriber_id}    ${subscription_id}=    Check Event Location Header    ${resp}

    ${resp}=    Delete Request Capif
    ...    /capif-events/v1/${subscriber_id}/subscriptions/${subscription_id}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    204    ${resp}

Deletes an individual CAPIF Event Subscription with invalid SubscriberId
    [Tags]    capif_api_events-4
    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Events Subscription
    ${resp}=    Post Request Capif
    ...    /capif-events/v1/${register_user_info_invoker['id']}/subscriptions
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    201    ${resp}

    ${subscriber_id}    ${subscription_id}=    Check Event Location Header    ${resp}

    ${resp}=    Delete Request Capif
    ...    /capif-events/v1/${SUBSCRIBER_ID_NOT_VALID}/subscriptions/${subscription_id}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    403    ${resp}
    Check Variable    ${resp.json()}    ProblemDetails
    Check Problem Details     ${resp}   status=403   detail=Event API not existing   cause=Event Subscriptions are not stored in CAPIF Database


Deletes an individual CAPIF Event Subscription with invalid SubscriptionId
    [Tags]    capif_api_events-5

    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${request_body}=    Create Events Subscription
    ${resp}=    Post Request Capif
    ...    /capif-events/v1/${register_user_info_invoker['id']}/subscriptions
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    201    ${resp}

    ${subscriber_id}    ${subscription_id}=    Check Event Location Header    ${resp}

    ${resp}=    Delete Request Capif
    ...    /capif-events/v1/${subscriber_id}/subscriptions/${SUBSCRIPTION_ID_NOT_VALID}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    404    ${resp}
    Check Variable    ${resp.json()}    ProblemDetails
    Check Problem Details     ${resp}   status=404   detail=Service API not existing   cause=Event API subscription id not found

