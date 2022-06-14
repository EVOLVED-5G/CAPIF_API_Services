*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Resource        /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagementRequests.robot
Library         /opt/robot-tests/tests/libraries/bodyRequests.py

Test Setup      Reset Testing Environment
# Test Setup    Initialize Test And Register    role=invoker


*** Variables ***
${API_INVOKER_NOT_REGISTERED}       not-valid


*** Test Cases ***
Discover Published service APIs by Authorised API Invoker
    [Tags]    capif_api_discover_service-1
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    # Publish one api
    ${request_body}=    Create Service Api Description
    ${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp}

    # Default Invoker Registration and Onboarding
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${resp}=    Get Request Capif
    ...    ${register_user_info_invoker['ccf_discover_url']}${register_user_info_invoker['apiInvokerId']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    200    ${resp}

    # Check returned values
    Should Not Be Empty    ${resp.json()}
    Length Should Be    ${resp.json()}    1

Discover Published service APIs by Non Authorised API Invoker
    [Tags]    capif_api_discover_service-2
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    # Publish one api
    ${request_body}=    Create Service Api Description
	 ${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp}

	#Register INVOKER
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    ${resp}=    Get Request Capif
    ...    ${register_user_info_invoker['ccf_discover_url']}${register_user_info_invoker['apiInvokerId']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

	Status Should Be    401    ${resp}

Discover Published service APIs by not registered API Invoker
    [Tags]    capif_api_discover_service-3
	#Register INVOKER
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

	 ${resp}=    Get Request Capif
    ...    ${register_user_info_invoker['ccf_discover_url']}${API_INVOKER_NOT_REGISTERED}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

	Status Should Be    403    ${resp}

Discover Published service APIs by registered API Invoker with 1 result filtered
    [Tags]    capif_api_discover_service-4
	#Register APF
    ${register_user_info}=    Publisher Default Registration

    ${api_name_1}=    Set Variable    apiName1
    ${api_name_2}=    Set Variable    apiName2

    # Publish 2 apis
    ${request_body}=    Create Service Api Description    ${api_name_1}
	${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

	Status Should Be    201    ${resp}

    ${request_body}=    Create Service Api Description    ${api_name_2}
	${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

	Status Should Be    201    ${resp}

    #Register INVOKER
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Request api 1
	 ${resp}=    Get Request Capif
    ...    ${register_user_info_invoker['ccf_discover_url']}${register_user_info_invoker['apiInvokerId']}&api-name=${api_name_1}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    200    ${resp}

    # Check returned values
    Should Not Be Empty    ${resp.json()}
    Length Should Be    ${resp.json()}    1

Discover Published service APIs by registered API Invoker filtered with no match
    [Tags]    capif_api_discover_service-5
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    ${api_name_1}=    Set Variable    apiName1
    ${api_name_2}=    Set Variable    apiName2

     # Publish 2 apis
    ${request_body}=    Create Service Api Description    ${api_name_1}
	${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

	Status Should Be    201    ${resp}

    ${request_body}=    Create Service Api Description    ${api_name_2}
	${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

	Status Should Be    201    ${resp}


    # Change to invoker role and register at api invoker management
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

	 # Request api 1
	 ${resp}=    Get Request Capif
    ...    ${register_user_info_invoker['ccf_discover_url']}${register_user_info_invoker['apiInvokerId']}&api-name=NOT_VALID_NAME
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    200    ${resp}

    # Check returned values
    Should Be Empty    ${resp.json()}

Discover Published service APIs by registered API Invoker not filtered
    [Tags]    capif_api_discover_service-6
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    ${api_name_1}=    Set Variable    apiName1
    ${api_name_2}=    Set Variable    apiName2

    # Publish 2 apis
    ${request_body}=    Create Service Api Description    ${api_name_1}
	${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

	Status Should Be    201    ${resp}

    ${request_body}=    Create Service Api Description    ${api_name_2}
	${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

	Status Should Be    201    ${resp}

    #Register INVOKER
    ${register_user_info_invoker}    ${url}    ${request_body}=    Invoker Default Onboarding

    # Request api 1
	 ${resp}=    Get Request Capif
    ...    ${register_user_info_invoker['ccf_discover_url']}${register_user_info_invoker['apiInvokerId']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    # Check returned values
    Should Not Be Empty    ${resp.json()}
    Length Should Be    ${resp.json()}    2
