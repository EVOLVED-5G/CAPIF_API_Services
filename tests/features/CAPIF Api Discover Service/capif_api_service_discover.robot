*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Resource    /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagementRequests.robot
Library     /opt/robot-tests/tests/libraries/bodyRequests.py


Test Setup    Initialize Test And Register    role=invoker

*** Variables ***
${API_INVOKER_NOT_REGISTERED}    not-valid

*** Keywords ***


*** Test Cases ***
Discover Published service APIs by Authorised API Invoker
	[Tags]     capif_api_discover_service-1
	[Setup]    Initialize Test And Register    role=apf

	# Publish one api
	${request_body}=    Create Service Api Description
	${resp}=            Post Request Capif                /published-apis/v1/${APF_ID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	# Change to user with invoker role and register to invoker management
	Register User At Jwt Auth    username=robot2    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	# Get api invoker id after regiter at api-invoker
	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	${resp}=    Get Request Capif    /service-apis/v1/allServiceAPIs?api-invoker-id=${api_invoker_id}

	Should Be Equal As Strings    ${resp.status_code}    200

	# Check returned values
	Should Not Be Empty    ${resp.json()}
	Length Should Be       ${resp.json()}    1

Discover Published service APIs by Non Authorised API Invoker
    [Tags]     capif_api_discover_service-2
    [Setup]    Initialize Test And Register    role=apf

	# Publish one api
    ${request_body}=    Create Service Api Description

	${resp}=    Post Request Capif    /published-apis/v1/${APF_ID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${apf_role_id}=    Set Variable    ${APF_ID}
	${apf_token}=      Set Variable    ${CAPIF_BEARER}

	# Change to user with invoker role and register to invoker management
	Register User At Jwt Auth    username=robot2    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	# Get api invoker id after regiter at api-invoker
	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	Get Token For User    username=robot    password=password    role=apf

	${resp}=    Get Request Capif    /service-apis/v1/allServiceAPIs?api-invoker-id=${api_invoker_id}

    Should Be Equal As Strings    ${resp.status_code}    401

Discover Published service APIs by not registered API Invoker
    [Tags]    capif_api_discover_service-3

    ${resp}=    Get Request Capif    /service-apis/v1/allServiceAPIs?api-invoker-id=${API_INVOKER_NOT_REGISTERED} 

    Should Be Equal As Strings    ${resp.status_code}    403

Discover Published service APIs by registered API Invoker with 1 result filtered
    [Tags]    capif_api_discover_service-4

	[Setup]    Initialize Test And Register    role=apf

	${api_name_1}=    Set Variable    apiName1
	${api_name_2}=    Set Variable    apiName2

	# Publish 2 apis
	${request_body}=    Create Service Api Description    ${api_name_1}
	${resp}=            Post Request Capif                /published-apis/v1/${APF_ID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${request_body}=    Create Service Api Description    ${api_name_2}
	${resp}=            Post Request Capif                /published-apis/v1/${APF_ID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	# Change to invoker role and register at api invoker management
	Register User At Jwt Auth    username=robot2    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	# Request api 1

    ${resp}=    Get Request Capif    /service-apis/v1/allServiceAPIs?api-invoker-id=${api_invoker_id}&api-name=${api_name_1}

    Should Be Equal As Strings    ${resp.status_code}    200

	# Check returned values
	Should Not Be Empty    ${resp.json()}
	Length Should Be       ${resp.json()}    1

Discover Published service APIs by registered API Invoker filtered with no match
	[Tags]     capif_api_discover_service-5
	[Setup]    Initialize Test And Register    role=apf

	${api_name_1}=    Set Variable    apiName1
	${api_name_2}=    Set Variable    apiName2

	# Publish 2 apis
	${request_body}=    Create Service Api Description    ${api_name_1}
	${resp}=            Post Request Capif                /published-apis/v1/${APF_ID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${request_body}=    Create Service Api Description    ${api_name_2}
	${resp}=            Post Request Capif                /published-apis/v1/${APF_ID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	# Change to invoker role and register at api invoker management
	Register User At Jwt Auth    username=robot2    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	# Request api 1

    ${resp}=    Get Request Capif    /service-apis/v1/allServiceAPIs?api-invoker-id=${api_invoker_id}&api-name=NOT_VALID_NAME

    Should Be Equal As Strings    ${resp.status_code}    200

	# Check returned values
	Should Be Empty    ${resp.json()}

Discover Published service APIs by registered API Invoker not filtered
	[Tags]     capif_api_discover_service-6
	[Setup]    Initialize Test And Register    role=apf

	${api_name_1}=    Set Variable    apiName1
	${api_name_2}=    Set Variable    apiName2

	# Publish 2 apis
	${request_body}=    Create Service Api Description    ${api_name_1}
	${resp}=            Post Request Capif                /published-apis/v1/${APF_ID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${request_body}=    Create Service Api Description    ${api_name_2}
	${resp}=            Post Request Capif                /published-apis/v1/${APF_ID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	# Change to invoker role and register at api invoker management
	Register User At Jwt Auth    username=robot2    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

    ${resp}=    Get Request Capif    /service-apis/v1/allServiceAPIs?api-invoker-id=${api_invoker_id}

    Should Be Equal As Strings    ${resp.status_code}    200

	# Check returned values
	Should Not Be Empty    ${resp.json()}
	Length Should Be       ${resp.json()}    2
