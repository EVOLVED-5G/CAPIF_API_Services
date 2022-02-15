*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Library     /opt/robot-tests/tests/libraries/bodyRequests.py
Resource    /opt/robot-tests/tests/resources/common/basicRequests.robot

Test Setup    Reset Db

*** Variables ***
${APF_ID_NOT_VALID}            apf-example
${SERVICE_API_ID_NOT_VALID}    not-valid
${API_INVOKER_NOT_VALID}       not-valid

*** Keywords ***


*** Test Cases ***
Create a security context for an API invoker
	[Tags]    capif_security_api-1

	Register User At Jwt Auth    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	${request_body}=    Create Service Security Body

	${resp}=    Put Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${url}=    Parse Url    ${resp.headers['Location']}

    Log                    ${url.path}
    Should Match Regexp    ${url.path}    ^/capif-security/v1/trustedInvokers/[0-9a-zA-Z]+

Create a security context for an API invoker wirh Invalid apiInvokerID
	[Tags]    capif_security_api-2

	Register User At Jwt Auth    role=invoker

	${request_body}=    Create Service Security Body

	${resp}=    Put Request Capif    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    403

Retrieve the Security Context of an API Invoker
	[Tags]    capif_security_api-3

	Register User At Jwt Auth    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	${request_body}=    Create Service Security Body

	${resp}=    Put Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${url}=    Parse Url    ${resp.headers['Location']}

    Log                    ${url.path}
    Should Match Regexp    ${url.path}    ^/capif-security/v1/trustedInvokers/[0-9a-zA-Z]+

	Register User At Jwt Auth    username=robot2    role=apf

	${resp}=    Get Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}

	Should Be Equal As Strings    ${resp.status_code}    200




