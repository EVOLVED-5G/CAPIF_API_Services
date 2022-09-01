*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
# Resource        /opt/robot-tests/tests/resources/api_invoker_management_requests/apiInvokerManagementRequests.robot
Library         /opt/robot-tests/tests/libraries/bodyRequests.py
Library         Process

Test Setup      Reset Testing Environment


*** Variables ***
${API_INVOKER_NOT_REGISTERED}       not-valid


*** Test Cases ***
Register Api Provider
    [Tags]    capif_api_provider_management-1
    # Send Onboarding Request
    ${request_body}=    Create Api Provider Enrolment Details Body

    ${resp}=    Post Request Capif
    ...    /api-provider-management/v1/registrations
    ...    json=${request_body}
    ...    server=http://${CAPIF_HOSTNAME}/

    Status Should Be    201    ${resp}
    # Store dummy signede certificate
    Store In File    ${INVOKER_USERNAME}.crt    ${resp.json()['onboardingInformation']['apiInvokerCertificate']}


