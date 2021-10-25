*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Resource    /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagemenrRequests.robot

*** Test Cases ***
Register NetApp
	[Tags]      tc-1
	${resp}=    Get Api Invoker Management UI
	# ${environment}=          Set Variable    jpu
	# ${test_session_name}=    Set Variable    MME_NODAL_1-OMEC

	# Wait Until Keyword Succeeds    5x    5    Test Server ${environment} Is Ready

	# ${statistics_file}    ${test_id}=    Launch Spirent Test And Get Statistic File    ${library}    ${test_session_name}    ${environment}    5

	# ${rate}=    Check Value Between Parameters From Excel    ${statistics_file}    SCTP    Socket Connect Count    value=1
