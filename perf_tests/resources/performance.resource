*** Variables ***

${ITERATIONS}           2
${THRESHOLD}            2.05

*** Keywords ***

Handle Timing
    [Arguments]     ${elapsed}       ${iteration}        ${average}      ${success}
    ${timespan}     Evaluate    ${elapsed.seconds}+(${elapsed.microseconds}/1000000.0)
    Log To Console  <<<[${TEST_NAME}]${iteration}=${timespan}>>>
    IF  ${timespan} < ${THRESHOLD}
        Log To Console  Success
        ${success}  Evaluate    ${success}+${1}
    ELSE
        Log To Console  Fail
    END
    IF  ${iteration} < ${1}
        ${average}=     Set Variable    ${timespan}
    ELSE
        ${average}=     Evaluate    ((${average}*(${iteration}))+${timespan})/${iteration+1}
    END
    [Return]    ${success}      ${average}

Handle End Results
    [Arguments]     ${success}      ${average}
    Log To Console      <<<[${TEST_NAME}];Success=${success}/${ITERATIONS};Average=${average}>>>
    IF      ${success} < ${ITERATIONS}
        Fail    Detected response times above threshold
    END