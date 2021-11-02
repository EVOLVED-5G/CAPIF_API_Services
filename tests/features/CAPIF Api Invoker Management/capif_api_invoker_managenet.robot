*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Resource    /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagemenrRequests.robot
Library     /opt/robot-tests/tests/libraries/api_invoker_management/bodyRequests.py

Library    MongoDBLibrary

Test Setup    Reset Db

*** Variables ***
${API_INVOKER_NOT_REGISTERED}    not-valid

*** Keywords ***
Reset Db
	Log                   Db capif.invokerdetails collection will be removed in order to isolate each test.
	Connect To MongoDB    mongodb://root:example@192.168.0.13	27017

	@{allCollections}=             Get MongoDB Collections    capif
	Log Many	@{allCollections}

	Drop MongoDB Collection    capif    invokerdetails

	Disconnect From MongoDB

*** Test Cases ***
Register NetApp
	[Tags]    tc-1

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

Register NetApp Already registered
	[Tags]    tc-2

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${resp}=    Post Request Capif    /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    403

Update Registered NetApp
	[Tags]    tc-3

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${url}=    Set Variable    ${resp.headers['Location']}

	${resp}=    Put Request Capif    ${url.path}    ${request_body}  server=${url.netloc}

	Should Be Equal As Strings    ${resp.status_code}    200

Update Not Registered NetApp
	[Tags]    tc-4

	${api_invoker_id}=    Set Variable    ${API_INVOKER_NOT_REGISTERED}

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Put Request Capif                      /api-invoker-management/v1/onboardedInvokers/${api_invoker_id}    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    404

Delete Registered NetApp
	[Tags]    tc-5

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json().get('apiInvokerId')}

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Delete Request Capif                   /api-invoker-management/v1/onboardedInvokers/${api_invoker_id}

	Should Be Equal As Strings    ${resp.status_code}    204

Delete Not Registered NetApp
	[Tags]    tc-6

	${api_invoker_id}=    Set Variable    ${API_INVOKER_NOT_REGISTERED}

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Delete Request Capif                   /api-invoker-management/v1/onboardedInvokers/${api_invoker_id}

	Should Be Equal As Strings    ${resp.status_code}    404

