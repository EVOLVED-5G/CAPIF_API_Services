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

Retrieve the Security Context of an API Invoker with invalid apiInvokerID
	[Tags]    capif_security_api-4

	Register User At Jwt Auth    username=robot2    role=apf

	${resp}=    Get Request Capif    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}

	Should Be Equal As Strings    ${resp.status_code}    404

Retrieve the Security Context of an API Invoker with invalid apfId
	[Tags]                 capif_security_api-5
	Set Global Variable    ${APF_ID}               ${APF_ID_NOT_VALID}

	${resp}=    Get Request Capif    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}

	Should Be Equal As Strings    ${resp.status_code}    403


Delete the Security Context of an API Invoker
	[Tags]                       capif_security_api-6
	Register User At Jwt Auth    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	${request_body}=    Create Service Security Body

	${resp}=    Put Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${resp}=    Delete Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}

	Should Be Equal As Strings    ${resp.status_code}    204


Delete the Security Context of an API Invoker with invalid apiInvokerID
	[Tags]                       capif_security_api-7
	Register User At Jwt Auth    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	${request_body}=    Create Service Security Body

	${resp}=    Put Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${resp}=    Delete Request Capif    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}

	Should Be Equal As Strings    ${resp.status_code}    403

Update the Security Context of an API Invoker
	[Tags]    capif_security_api-8

	Register User At Jwt Auth    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	${request_body}=    Create Service Security Body

	${resp}=    Put Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${resp}=    Post Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}/update    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    200

Update the Security Context of an API Invoker with invalid apiInvokerID
	[Tags]    capif_security_api-9

	Register User At Jwt Auth    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	${request_body}=    Create Service Security Body

	${resp}=    Put Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${resp}=    Post Request Capif    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}/update    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    403

Revoke the authorization of the API invoker for APIs
	[Tags]    capif_security_api-10

	Register User At Jwt Auth    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	${request_body}=    Create Service Security Body

	${resp}=    Put Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	Register User At Jwt Auth    username=robot2    role=apf

	${request_body}=    Create Security Notification Body    ${api_invoker_id}

	${resp}=    Post Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}/delete    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    204

Revoke the authorization of the API invoker for APIs without valid apfID.
	[Tags]                       capif_security_api-11
	Register User At Jwt Auth    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	${request_body}=    Create Service Security Body

	${resp}=    Put Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	Set Global Variable    ${APF_ID}    ${APF_ID_NOT_VALID}

	${request_body}=    Create Security Notification Body    ${api_invoker_id}

	${resp}=    Post Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}/delete    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    403

Revoke the authorization of the API invoker for APIs with invalid apiInvokerId
	[Tags]                       capif_security_api-12
	Register User At Jwt Auth    username=robot2          role=apf

	${request_body}=    Create Security Notification Body    ${API_INVOKER_NOT_VALID}

	${resp}=    Post Request Capif    /capif-security/v1/trustedInvokers/${API_INVOKER_NOT_VALID}/delete    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    404

Retrieve access token
	[Tags]                       capif_security_api-13
	Register User At Jwt Auth    role=invoker

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}

	${request_body}=    Create Service Security Body

	${resp}=    Put Request Capif    /capif-security/v1/trustedInvokers/${api_invoker_id}    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    201

	${request_body}=    Create Access Token Req Body

	${resp}=    Post Request Capif    /capif-security/v1/securities/${api_invoker_id}/token    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    200

Retrieve access token with invalid apiInvokerId
	[Tags]    capif_security_api-14
	Register User At Jwt Auth    role=invoker

	${request_body}=    Create Access Token Req Body

	${resp}=    Post Request Capif    /capif-security/v1/securities/${API_INVOKER_NOT_VALID}/token    ${request_body}

	Should Be Equal As Strings    ${resp.status_code}    403
