*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Resource    /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagementRequests.robot
Library     /opt/robot-tests/tests/libraries/bodyRequests.py


Test Setup    Initialize Test And Register    role=invoker    db_col=invokerdetails

*** Variables ***
${API_INVOKER_NOT_REGISTERED}    not-valid

*** Keywords ***


*** Test Cases ***
Discover Published service APIs by Authorised API Invoker
	[Tags]     capif_api_discover_service-1
	[Setup]    Initialize Test And Register    role=apf    db_col=invokerdetails

	${request_body}=    Create Service Api Description
	${resp}=            Post Request Capif                /published-apis/v1/${APF_ID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201


	Register User At Jwt Auth    username=robot2    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	${resp}=    Get Request Capif    /service-apis/v1/allServiceAPIs?api-invoker-id=${api_invoker_id}

	Should Be Equal As Strings    ${resp.status_code}    200

Discover Published service APIs by Non Authorised API Invoker
    [Tags]     capif_api_discover_service-2
    [Setup]    Initialize Test And Register    role=apf    db_col=invokerdetails
    ${request_body}=    Create Service Api Description

	${resp}=    Post Request Capif    /published-apis/v1/${APF_ID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${apf_role_id}=    Set Variable    ${APF_ID}
	${apf_token}=      Set Variable    ${CAPIF_BEARER}

	Register User At Jwt Auth    username=robot2    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	Get Token For User    username=robot    password=password   role=apf

	${resp}=    Get Request Capif    /service-apis/v1/allServiceAPIs?api-invoker-id=${api_invoker_id}

    Should Be Equal As Strings    ${resp.status_code}    401

# Discover Not Published service APIs by Authorised API Invoker
#    [Tags]    capif_api_discover_service-3

#    ${resp}=    Get Request Capif    /allServiceAPIs?api-invoker-id=${API_INVOKER_NOT_REGISTERED} 

#    Should Be Equal As Strings    ${resp.status_code}    404


