*** Settings ***
Library    OperatingSystem
Library    String

*** Variables ***
${CONFIG_FILE}    config.ini

*** Test Cases ***
Run Dynamic Calculator
    ${content}=    Get File    ${CONFIG_FILE}
    ${a}=    Get Config Value    ${content}    a
    ${b}=    Get Config Value    ${content}    b

    Should Not Be Empty    ${a}
    Should Not Be Empty    ${b}

    ${sum}=    Add Numbers    ${a}    ${b}
    ${diff}=    Subtract Numbers    ${a}    ${b}
    ${prod}=    Multiply Numbers    ${a}    ${b}
    ${quot}=    Divide Numbers    ${a}    ${b}

    Log To Console    Input A: ${a}
    Log To Console    Input B: ${b}
    Log To Console    Add: ${sum}
    Log To Console    Subtract: ${diff}
    Log To Console    Multiply: ${prod}
    Log To Console    Divide: ${quot}

*** Keywords ***
Get Config Value
    [Arguments]    ${content}    ${key}
    ${lines}=    Split To Lines    ${content}
    FOR    ${line}    IN    @{lines}
        ${trimmed}=    Strip String    ${line}
        ${is_comment}=    Run Keyword And Return Status    Should Start With    ${trimmed}    #
        ${is_section}=    Run Keyword And Return Status    Should Start With    ${trimmed}    [
        IF    '${trimmed}' != '' and not ${is_comment} and not ${is_section}
            ${parts}=    Split String    ${trimmed}    =    maxsplit=1
            IF    '${parts[0].strip()}' == '${key}'
                RETURN    ${parts[1].strip()}
            END
        END
    END
    RETURN    ${EMPTY}

Add Numbers
    [Arguments]    ${a}    ${b}
    ${A}=    Convert To Number    ${a}
    ${B}=    Convert To Number    ${b}
    ${result}=    Evaluate    ${A} + ${B}
    [Return]    ${result}

Subtract Numbers
    [Arguments]    ${a}    ${b}
    ${A}=    Convert To Number    ${a}
    ${B}=    Convert To Number    ${b}
    ${result}=    Evaluate    ${A} - ${B}
    [Return]    ${result}

Multiply Numbers
    [Arguments]    ${a}    ${b}
    ${A}=    Convert To Number    ${a}
    ${B}=    Convert To Number    ${b}
    ${result}=    Evaluate    ${A} * ${B}
    [Return]    ${result}

Divide Numbers
    [Arguments]    ${a}    ${b}
    ${A}=    Convert To Number    ${a}
    ${B}=    Convert To Number    ${b}
    ${result}=    Evaluate    ${A} / ${B}
    [Return]    ${result}
