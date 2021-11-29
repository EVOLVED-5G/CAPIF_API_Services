*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Resource    /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagemenrRequests.robot
Library     /opt/robot-tests/tests/libraries/api_invoker_management/bodyRequests.py

Test Setup    Initialize Test And Register    role=apf    db_col=serviceapidescriptions

*** Variables ***
${API_INVOKER_NOT_REGISTERED}    not-valid
${APF_ID_NOT_VALID}              apf-example

*** Keywords ***


*** Test Cases ***
Publish API by Authorised API Publisher
	[Tags]    capif_api_publish_service-1

	${request_body}=    Create Service Api Description
	${resp}=            Post Request Capif                /published-apis/v1/${APF_ID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

Publish API by NON Authorised API Publisher
	[Tags]              capif_api_publish_service-2
	${request_body}=    Create Service Api Description
	${resp}=            Post Request Capif                /published-apis/v1/${APF_ID_NOT_VALID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    401

Retrieve all APIs Published by Authorised apfId
	[Tags]    capif_api_publish_service-3

	${request_body}=    Create Service Api Description
	${resp}=            Post Request Capif                /published-apis/v1/${APF_ID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${request_body}=    Create Service Api Description    other_service
	${resp}=            Post Request Capif                /published-apis/v1/${APF_ID}/service-apis    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201


	${resp}=    Get Request Capif    /published-apis/v1/${APF_ID}/service-apis

	Should Be Equal As Strings    ${resp.status_code}    200

	Log    ${resp.json()}

Retrieve all APIs Published by NON Authorised apfId
	[Tags]    capif_api_publish_service-4

	Log     Test "${TEST NAME}" Not Implemented    WARN
	Skip    Test "${TEST NAME}" Not Implemented

Retrieve single APIs Published by Authorised apfId
	[Tags]    capif_api_publish_service-5

	Log     Test "${TEST NAME}" Not Implemented    WARN
	Skip    Test "${TEST NAME}" Not Implemented

Retrieve single APIs non Published by Authorised apfId
	[Tags]    capif_api_publish_service-6

	Log     Test "${TEST NAME}" Not Implemented    WARN
	Skip    Test "${TEST NAME}" Not Implemented

Retrieve single APIs Published by NON Authorised apfId
	[Tags]    capif_api_publish_service-7

	Log     Test "${TEST NAME}" Not Implemented    WARN
	Skip    Test "${TEST NAME}" Not Implemented

Update API Published by Authorised apfId with valid serviceApiId
	[Tags]    capif_api_publish_service-8

	Log     Test "${TEST NAME}" Not Implemented    WARN
	Skip    Test "${TEST NAME}" Not Implemented

Update APIs Published by Authorised apfId with invalid serviceApiId
	[Tags]    capif_api_publish_service-9

	Log     Test "${TEST NAME}" Not Implemented    WARN
	Skip    Test "${TEST NAME}" Not Implemented

Update APIs Published by NON Authorised apfId
	[Tags]    capif_api_publish_service-10

	Log     Test "${TEST NAME}" Not Implemented    WARN
	Skip    Test "${TEST NAME}" Not Implemented

Delete API Published by Authorised apfId with valid serviceApiId
	[Tags]    capif_api_publish_service-11

	Log     Test "${TEST NAME}" Not Implemented    WARN
	Skip    Test "${TEST NAME}" Not Implemented

Delete APIs Published by Authorised apfId with invalid serviceApiId
	[Tags]    capif_api_publish_service-12

	Log     Test "${TEST NAME}" Not Implemented    WARN
	Skip    Test "${TEST NAME}" Not Implemented

Delete APIs Published by NON Authorised apfId
	[Tags]    capif_api_publish_service-13

	Log     Test "${TEST NAME}" Not Implemented    WARN
	Skip    Test "${TEST NAME}" Not Implemented


