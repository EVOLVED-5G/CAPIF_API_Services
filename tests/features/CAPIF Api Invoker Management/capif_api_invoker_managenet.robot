*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Resource    /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagementRequests.robot
Library     /opt/robot-tests/tests/libraries/api_invoker_management/bodyRequests.py

Test Setup    Initialize Test And Register    role=invoker    db_col=invokerdetails

*** Variables ***
${API_INVOKER_NOT_REGISTERED}    not-valid

*** Keywords ***


*** Test Cases ***
Register NetApp
	[Tags]    capif_api_invoker_management-1

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

Register NetApp Already registered
	[Tags]    capif_api_invoker_management-2

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${resp}=    Post Request Capif    /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    403

Update Registered NetApp
	[Tags]    capif_api_invoker_management-3

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${url}=    Parse Url    ${resp.headers['Location']}

	${resp}=    Put Request Capif    ${url.path}    ${request_body}    server=${url.scheme}://${url.netloc}

	Should Be Equal As Strings    ${resp.status_code}    200

Update Not Registered NetApp
	[Tags]    capif_api_invoker_management-4

	${api_invoker_id}=    Set Variable    ${API_INVOKER_NOT_REGISTERED}

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Put Request Capif                      /api-invoker-management/v1/onboardedInvokers/${api_invoker_id}    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    404

Delete Registered NetApp
	[Tags]    capif_api_invoker_management-5

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${url}=    Parse Url    ${resp.headers['Location']}

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Delete Request Capif                   ${url.path}    server=${url.scheme}://${url.netloc}

	Should Be Equal As Strings    ${resp.status_code}    204

Delete Not Registered NetApp
	[Tags]    capif_api_invoker_management-6

	${api_invoker_id}=    Set Variable    ${API_INVOKER_NOT_REGISTERED}

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Delete Request Capif                   /api-invoker-management/v1/onboardedInvokers/${api_invoker_id}

	Should Be Equal As Strings    ${resp.status_code}    404


