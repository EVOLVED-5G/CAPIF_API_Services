*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Resource        /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagementRequests.robot
Resource        ../../resources/common.resource
Resource        ../../resources/performance.resource
Library         /opt/robot-tests/tests/libraries/bodyRequests.py

Test Setup      Reset Testing Environment
# Test Setup    Initialize Test And Register    role=invoker


*** Variables ***
${API_INVOKER_NOT_REGISTERED}       not-valid


*** Test Cases ***
Discover Published service APIs by Authorised API Invoker Performance
    [Tags]    capif_api_discover_service-1
    #Register APF
    ${register_user_info}=    Provider Default Registration

    # Publish one api
    ${service_api_description_published}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}

    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Test
    ${success}=     Set Variable    ${0}
    ${average}=     Set Variable    ${0}

    FOR     ${index}    IN RANGE    ${ITERATIONS}
        Log To Console      \nIteration: ${index}

        ${resp}=    Get Request Capif
        ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}&aef-id=${register_user_info['aef_id']}
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${INVOKER_USERNAME}

        Check Response Variable Type And Values    ${resp}    200    DiscoveredAPIs

        # Check Results
        Dictionary Should Contain Key    ${resp.json()}    serviceAPIDescriptions
        Should Not Be Empty    ${resp.json()['serviceAPIDescriptions']}
        Length Should Be    ${resp.json()['serviceAPIDescriptions']}    1
        List Should Contain Value   ${resp.json()['serviceAPIDescriptions']}    ${service_api_description_published}

        ${success}       ${average}      Handle Timing       ${resp.elapsed}     ${index}    ${average}      ${success}
    END

    Handle End Results      ${success}      ${average}

Discover Published service APIs by registered API Invoker with 1 result filtered performance
    [Tags]    capif_api_discover_service-4
    #Register APF
    ${register_user_info}=    Provider Default Registration

    ${api_name_1}=    Set Variable    service_1
    ${api_name_2}=    Set Variable    service_2

    # Publish 2 apis
    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    ${api_name_1}
    ${service_api_description_published_2}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    ${api_name_2}

    # Register INVOKER
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Request all APIs for Invoker
    ${resp}=    Get Request Capif
    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}&aef-id=${register_user_info['aef_id']}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Check Response Variable Type And Values    ${resp}    200    DiscoveredAPIs

    # Check returned values
    Should Not Be Empty    ${resp.json()['serviceAPIDescriptions']}
    Length Should Be    ${resp.json()['serviceAPIDescriptions']}    2
    List Should Contain Value   ${resp.json()['serviceAPIDescriptions']}    ${service_api_description_published_1}
    List Should Contain Value   ${resp.json()['serviceAPIDescriptions']}    ${service_api_description_published_2}

    # Request api 1
    ${success}=     Set Variable    ${0}
    ${average}=     Set Variable    ${0}

    FOR     ${index}    IN RANGE    ${ITERATIONS}
        Log To Console      \nIteration: ${index}

        ${resp}=    Get Request Capif
        ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}&api-name=${api_name_1}
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${INVOKER_USERNAME}

        Check Response Variable Type And Values    ${resp}    200    DiscoveredAPIs

        # Check Results
        Should Not Be Empty    ${resp.json()['serviceAPIDescriptions']}
        Length Should Be    ${resp.json()['serviceAPIDescriptions']}    1
        List Should Contain Value    ${resp.json()['serviceAPIDescriptions']}    ${service_api_description_published_1}

        ${success}       ${average}      Handle Timing       ${resp.elapsed}     ${index}    ${average}      ${success}
    END

    Handle End Results      ${success}      ${average}


Discover Published service APIs by registered API Invoker filtered with no match performance
    [Tags]    capif_api_discover_service-5
    #Register APF
    ${register_user_info}=    Provider Default Registration

    ${api_name_1}=    Set Variable    apiName1
    ${api_name_2}=    Set Variable    apiName2

    # Publish 2 apis
    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    ${api_name_1}
    ${service_api_description_published_2}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    ${api_name_2}

    # Change to invoker role and register at api invoker management
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Request all APIs for Invoker
    ${resp}=    Get Request Capif
    ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}&aef-id=${register_user_info['aef_id']}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Check Response Variable Type And Values    ${resp}    200    DiscoveredAPIs

    # Check returned values
    Should Not Be Empty    ${resp.json()['serviceAPIDescriptions']}
    Length Should Be    ${resp.json()['serviceAPIDescriptions']}    2
    List Should Contain Value   ${resp.json()['serviceAPIDescriptions']}    ${service_api_description_published_1}
    List Should Contain Value   ${resp.json()['serviceAPIDescriptions']}    ${service_api_description_published_2}

    # Request api 1
    ${success}=     Set Variable    ${0}
    ${average}=     Set Variable    ${0}

    FOR     ${index}    IN RANGE    ${ITERATIONS}
        Log To Console      \nIteration: ${index}

        ${resp}=    Get Request Capif
        ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}&api-name=NOT_VALID_NAME
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${INVOKER_USERNAME}

        # Check Results
        Check Response Variable Type And Values    ${resp}    404    ProblemDetails
        ...    title=Not Found
        ...    status=404
        ...    detail=API Invoker ${register_user_info_invoker['api_invoker_id']} has no API Published that accomplish filter conditions
        ...    cause=No API Published accomplish filter conditions

        ${success}       ${average}      Handle Timing       ${resp.elapsed}     ${index}    ${average}      ${success}
    END

    Handle End Results      ${success}      ${average}

Discover Published service APIs by registered API Invoker not filtered performance
    [Tags]    capif_api_discover_service-6
    #Register APF
    ${register_user_info}=    Provider Default Registration

    ${api_name_1}=    Set Variable    apiName1
    ${api_name_2}=    Set Variable    apiName2

    # Publish 2 apis
    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    ${api_name_1}
    ${service_api_description_published_2}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    ${api_name_2}

    # Change to invoker role and register at api invoker management
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Request all APIs for Invoker
    ${success}=     Set Variable    ${0}
    ${average}=     Set Variable    ${0}

    FOR     ${index}    IN RANGE    ${ITERATIONS}
        Log To Console      \nIteration: ${index}

        ${resp}=    Get Request Capif
        ...    ${DISCOVER_URL}${register_user_info_invoker['api_invoker_id']}&aef-id=${register_user_info['aef_id']}
        ...    server=${CAPIF_HTTPS_URL}
        ...    verify=ca.crt
        ...    username=${INVOKER_USERNAME}

        Check Response Variable Type And Values    ${resp}    200    DiscoveredAPIs

        # Check Results
        Should Not Be Empty    ${resp.json()['serviceAPIDescriptions']}
        Length Should Be    ${resp.json()['serviceAPIDescriptions']}    2
        List Should Contain Value   ${resp.json()['serviceAPIDescriptions']}    ${service_api_description_published_1}
        List Should Contain Value   ${resp.json()['serviceAPIDescriptions']}    ${service_api_description_published_2}

        ${success}       ${average}      Handle Timing       ${resp.elapsed}     ${index}    ${average}      ${success}
    END

    Handle End Results      ${success}      ${average}