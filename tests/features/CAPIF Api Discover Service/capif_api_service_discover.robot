*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Resource    /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagementRequests.robot
Library     /opt/robot-tests/tests/libraries/api_invoker_management/bodyRequests.py

Test Setup    Initialize Test And Register    role=invoker    db_col=invokerdetails

*** Variables ***
${API_INVOKER_NOT_REGISTERED}    not-valid

*** Keywords ***


*** Test Cases ***
# Discover Published service APIs by Authorised API Invoker
# 	[Tags]    capif_api_discover_service-1

# 	${request_body}=    Create Onboarding Notification Body
# 	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

# 	Should Be Equal As Strings    ${resp.status_code}    201

# 	${resp}=   Get Request Capif  /allServiceAPIs?api-invoker-id=${resp.json()['apiInvokerId']}

# 	Should Be Equal As Strings    ${resp.status_code}    200

# 	Log Many    ${resp.json()}

# Discover Published service APIs by Non Authorised API Invoker
# 	[Tags]    capif_api_discover_service-2
	
# 	${request_body}=    Create Onboarding Notification Body
# 	${resp}=            Post Request Capif                     /api-invoker-management/v1/onboardedInvokers    ${request_body}

# 	Register User At Jwt Auth    username=robot2    role=apf

# 	${resp}=   Get Request Capif  /allServiceAPIs?api-invoker-id=${API_INVOKER_NOT_REGISTERED} 

# 	Should Be Equal As Strings    ${resp.status_code}    401

# Discover Not Published service APIs by Authorised API Invoker
# 	[Tags]    capif_api_discover_service-3

# 	${resp}=   Get Request Capif  /allServiceAPIs?api-invoker-id=${API_INVOKER_NOT_REGISTERED} 

# 	Should Be Equal As Strings    ${resp.status_code}    404


