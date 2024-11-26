*** Settings ***
Library     /opt/robot-tests/tests/libraries/helpers.py
Resource    /opt/robot-tests/tests/resources/common/basicRequests.robot


*** Variables ***
${INVOKER_USERNAME}             ROBOT_TESTING_INVOKER
${PROVIDER_USERNAME}            ROBOT_TESTING_PROVIDER
${APF_PROVIDER_USERNAME}        APF_${PROVIDER_USERNAME}
${AEF_PROVIDER_USERNAME}        AEF_${PROVIDER_USERNAME}
${AMF_PROVIDER_USERNAME}        AMF_${PROVIDER_USERNAME}

${INVOKER_NOT_REGISTERED}       not-valid
${INVOKER_ROLE}                 invoker
${PROVIDER_ROLE}                provider

${CAPIF_HOSTNAME}               capifcore
${CAPIF_HTTP_PORT}
${CAPIF_HTTPS_PORT}
${CAPIF_IP}                     127.0.0.1
${CAPIF_CALLBACK_IP}            host.docker.internal
${CAPIF_CALLBACK_PORT}          8086

${DISCOVER_URL}                 /service-apis/v1/allServiceAPIs?api-invoker-id=


*** Keywords ***
Reset Testing Environment
    Log    Db capif.invokerdetails collection will be removed in order to isolate each test.

    Clean Test Information By HTTP Requests

Check Location Header
    [Documentation]    This keyword will check location header at response according to regular expression provided as argument
    [Arguments]    ${resp}    ${regular_expression}

    ${event_url}=    Parse Url    ${resp.headers['Location']}

    Should Match Regexp    ${event_url.path}    ${regular_expression}
    RETURN    ${event_url}

Check Event Location Header
    [Arguments]    ${resp}

    ${event_url}=    Check Location Header    ${resp}    ${LOCATION_EVENT_RESOURCE_REGEX}

    ${subscriber_id}    ${subscription_id}=    Get Subscriber And Subscription From Location    ${event_url.path}

    RETURN    ${subscriber_id}    ${subscription_id}

Check Problem Details
    [Arguments]    ${resp}    &{input_parameters}
    Check Variable    ${resp.json()}    ProblemDetails
    FOR    ${input}    IN    @{input_parameters}
        Log    ${input}=${input_parameters['${input}']}
        Should Match    "${resp.json()['${input}']}"    "${input_parameters['${input}']}"
    END

Check Response Variable Type And Values
    [Arguments]    ${resp}    ${status_code}    ${variable_type}    &{input_parameters}
    Status Should Be    ${status_code}    ${resp}
    Check Variable    ${resp.json()}    ${variable_type}
    FOR    ${input}    IN    @{input_parameters}
        Log    ${input}=${input_parameters['${input}']}
        Should Match Regexp    "${resp.json()['${input}']}"    "${input_parameters['${input}']}"
    END

Remove Keys From Object
    [Arguments]    ${input}    @{keys_to_remove}

    ${filtered_input}=    Remove Keys From Object Helper    ${input}    ${keys_to_remove}

    RETURN    ${filtered_input}

Test ${TEST NAME} Currently Not Supported
    Log    Test "${TEST NAME}" Currently not supported    WARN
    Skip    Test "${TEST NAME}" Currently not supported
