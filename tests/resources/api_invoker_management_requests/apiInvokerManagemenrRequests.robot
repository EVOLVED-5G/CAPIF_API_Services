*** Settings ***
Resource    /opt/robot-tests/tests/resources/common.resource
Resource    /opt/robot-tests/tests/resources/common/basicRequests.robot



*** Keywords ***
Get Api Invoker Management UI
    [Arguments]

    ${resp}=    Get Request Capif    /api-invoker-management/v1/ui/

    Should Be Equal As Strings    ${resp.status_code}    200

    [Return]    ${resp.json()}

