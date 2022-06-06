*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Resource    /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagementRequests.robot
Library     /opt/robot-tests/tests/libraries/api_invoker_management/bodyRequests.py
Library    Process

Test Setup    Initialize Test And Register    role=invoker

*** Variables ***
${API_INVOKER_NOT_REGISTERED}    not-valid

*** Keywords ***
Testing Teardown
    Run Process     cp     dummy.crt   /opt/robot-tests/results/
	Run Process     cp     private.key   /opt/robot-tests/results/
	Run Process     cp     cert_req.csr   /opt/robot-tests/results/



*** Test Cases ***
TestJMS
    [Tags]     jms_test
	[Setup]    Testing Teardown
	Setup Core Name   127.0.0.1  capifcore
	Reset Db

    
	${cn}=    Set Variable      robot_dummy

	# Create certificate and private_key for this machine.
	${csr_request}=    Create Csr     cert_req.csr  private.key   ${cn}


	# Obtain ca root certificate
    ${resp}=    Get Request Capif    /ca-root
	Status Should Be                 201    ${resp}
	Log   ${resp.json()['certificate']}
	Store Ca Root    ca.crt    ${resp.json()['certificate']}
	${result}=   Run Process      ls
	Log    ${result.stdout}	
	${result}=   Run Process   cat    -A   ca.crt
    Log    ${result.stdout}
    

	#Register Netapp
	${access_token}    ${netappID}   ${ccf_onboarding_url}   ${ccf_discover_url}=    Register User At Jwt Auth   cn=${cn}
    
	
    ${capif_ip}=    Set Variable   capifcore
	${capif_callback_ip}=    Set Variable   host.docker.internal
    ${capif_callback_port}=    Set Variable   8086

	${csr_request_str}=   Convert To String     ${csr_request}

    # On Boarding
	# ${csr_request_value}=    Set Variable     ${csr_request.decode('utf-8')}  
	${request_body}=    Create Onboarding Notification Body New    http://${capif_callback_ip}:${capif_callback_port}/netapp_callback    ${csr_request}

	${resp}=            Post Request Capif Cert                   ${ccf_onboarding_url}    data=${request_body}    server=https://${capif_ip}/      verify=ca.crt
    # ${api_invoker_id}=  Onboard Netapp To Capif   ${capif_ip}    ${capif_callback_ip}  ${capif_callback_port}    ${access_token}   ${ccf_onboarding_url}

	Status Should Be                 201    ${resp}
	${api_invoker_id}=    Set Variable    ${resp.json()['apiInvokerId']}
	# Store dummy signede certificate
	Store Ca Root   dummy.crt     ${resp.json()['onboardingInformation']['apiInvokerCertificate']}

	${result}=   Run Process   cat    dummy.crt
    Log    ${result.stdout}

    Run Process     cp     dummy.crt   /opt/robot-tests/results/
	Run Process     cp     private.key   /opt/robot-tests/results/
	Run Process     cp     cert_req.csr   /opt/robot-tests/results/

    # Execute discover
	${cert}=   Cert Tuple    dummy.crt    private.key
	${resp}=   Get Request Capif Cert  ${ccf_discover_url}${api_invoker_id}  server=https://${capif_ip}/  verify=ca.crt   cert=${cert}
	Status Should Be                 200    ${resp}

    # Discover Service Apis    ${capif_ip}    ${api_invoker_id}    ${access_token}    ${ccf_discover_url}




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

	${resp}=    Put Request Capif    ${url.path}    ${request_body}    server=${NGINX_HOSTNAME}

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
	${resp}=            Delete Request Capif                   ${url.path}    server=${NGINX_HOSTNAME}

	Should Be Equal As Strings    ${resp.status_code}    204

Delete Not Registered NetApp
	[Tags]    capif_api_invoker_management-6

	${api_invoker_id}=    Set Variable    ${API_INVOKER_NOT_REGISTERED}

	${request_body}=    Create Onboarding Notification Body
	${resp}=            Delete Request Capif                   /api-invoker-management/v1/onboardedInvokers/${api_invoker_id}

	Should Be Equal As Strings    ${resp.status_code}    404


