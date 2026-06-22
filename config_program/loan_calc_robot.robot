*** Settings ***
Library    OperatingSystem
Library    String
Library    Collections

*** Variables ***
${CONFIG_FILE}    config.ini

*** Test Cases ***
test_loan_calculator_config_file_exists
    [Documentation]    Test that config file was successfully read.
    ${content}=    Get File    ${CONFIG_FILE}
    Should Not Be Empty    ${content}

test_loan_calculator_read_inputs
    [Documentation]    Test that loan inputs can be read from config file.
    ${content}=    Get File    ${CONFIG_FILE}
    ${principal}=    Get Config Value    ${content}    principal
    ${annual_rate}=    Get Config Value    ${content}    annual_rate
    ${years}=    Get Config Value    ${content}    years
    
    Should Not Be Empty    ${principal}
    Should Not Be Empty    ${annual_rate}
    Should Not Be Empty    ${years}

test_loan_calculator_inputs_are_valid
    [Documentation]    Test that loan inputs are valid numeric values.
    ${content}=    Get File    ${CONFIG_FILE}
    ${principal}=    Get Config Value    ${content}    principal
    ${annual_rate}=    Get Config Value    ${content}    annual_rate
    ${years}=    Get Config Value    ${content}    years
    
    ${principal_num}=    Convert To Number    ${principal}
    ${annual_rate_num}=    Convert To Number    ${annual_rate}
    ${years_num}=    Convert To Integer    ${years}
    
    Should Be True    ${principal_num} > 0    Principal must be positive
    Should Be True    ${annual_rate_num} >= 0    Annual rate must be non-negative
    Should Be True    ${years_num} > 0    Years must be positive

test_loan_calculator_emi_calculation
    [Documentation]    Test EMI calculation.
    ${content}=    Get File    ${CONFIG_FILE}
    ${principal}=    Get Config Value    ${content}    principal
    ${annual_rate}=    Get Config Value    ${content}    annual_rate
    ${years}=    Get Config Value    ${content}    years
    
    ${months}=    Evaluate    int(${years}) * 12
    ${monthly_rate}=    Evaluate    float(${annual_rate}) / 100.0 / 12.0
    
    ${emi}=    Calculate EMI    ${principal}    ${monthly_rate}    ${months}
    
    Should Not Be Empty    ${emi}
    ${emi_num}=    Convert To Number    ${emi}
    Should Be True    ${emi_num} > 0    EMI should be positive
    Log To Console    EMI Calculation: ${principal} @ ${annual_rate}% for ${years} years = ${emi} per month

test_loan_calculator_total_payment
    [Documentation]    Test total payment calculation.
    ${content}=    Get File    ${CONFIG_FILE}
    ${principal}=    Get Config Value    ${content}    principal
    ${annual_rate}=    Get Config Value    ${content}    annual_rate
    ${years}=    Get Config Value    ${content}    years
    
    ${months}=    Evaluate    int(${years}) * 12
    ${monthly_rate}=    Evaluate    float(${annual_rate}) / 100.0 / 12.0
    
    ${emi}=    Calculate EMI    ${principal}    ${monthly_rate}    ${months}
    ${total_payment}=    Calculate Total Payment    ${emi}    ${months}
    
    Should Not Be Empty    ${total_payment}
    ${total_payment_num}=    Convert To Number    ${total_payment}
    ${principal_num}=    Convert To Number    ${principal}
    Should Be True    ${total_payment_num} >= ${principal_num}    Total payment should be >= principal
    Log To Console    Total Payment: ${total_payment}

test_loan_calculator_interest_calculation
    [Documentation]    Test interest (extra amount) calculation.
    ${content}=    Get File    ${CONFIG_FILE}
    ${principal}=    Get Config Value    ${content}    principal
    ${annual_rate}=    Get Config Value    ${content}    annual_rate
    ${years}=    Get Config Value    ${content}    years
    
    ${months}=    Evaluate    int(${years}) * 12
    ${monthly_rate}=    Evaluate    float(${annual_rate}) / 100.0 / 12.0
    
    ${emi}=    Calculate EMI    ${principal}    ${monthly_rate}    ${months}
    ${total_payment}=    Calculate Total Payment    ${emi}    ${months}
    ${total_interest}=    Calculate Total Interest    ${total_payment}    ${principal}
    
    Should Not Be Empty    ${total_interest}
    ${total_interest_num}=    Convert To Number    ${total_interest}
    Should Be True    ${total_interest_num} >= 0    Total interest should be non-negative
    Log To Console    Total Interest: ${total_interest}

test_loan_calculator_months_calculation
    [Documentation]    Test months calculation from years.
    ${content}=    Get File    ${CONFIG_FILE}
    ${years}=    Get Config Value    ${content}    years
    
    ${months}=    Evaluate    int(${years}) * 12
    ${expected_months}=    Evaluate    int(${years}) * 12
    
    Should Be Equal As Numbers    ${months}    ${expected_months}

test_loan_calculator_all_calculations
    [Documentation]    Test all loan calculations together.
    ${content}=    Get File    ${CONFIG_FILE}
    ${principal}=    Get Config Value    ${content}    principal
    ${annual_rate}=    Get Config Value    ${content}    annual_rate
    ${years}=    Get Config Value    ${content}    years
    
    ${months}=    Evaluate    int(${years}) * 12
    ${monthly_rate}=    Evaluate    float(${annual_rate}) / 100.0 / 12.0
    
    ${emi}=    Calculate EMI    ${principal}    ${monthly_rate}    ${months}
    ${total_payment}=    Calculate Total Payment    ${emi}    ${months}
    ${total_interest}=    Calculate Total Interest    ${total_payment}    ${principal}
    
    Log To Console    \n===============================================
    Log To Console    CONFIG-DRIVEN LOAN CALCULATOR
    Log To Console    ===============================================
    Log To Console    Principal (borrowed) = ${principal}
    Log To Console    Annual rate          = ${annual_rate} %
    Log To Console    Years                = ${years} (${months} months)
    Log To Console    -----------------------------------------------
    Log To Console    Monthly EMI          = ${emi}
    Log To Console    Total payment        = ${total_payment} (principal + interest)
    Log To Console    EXTRA amount paid    = ${total_interest} (interest only, on top of the ${principal} you borrowed)
    Log To Console    ===============================================
    
    Should Not Be Empty    ${principal}
    Should Not Be Empty    ${emi}
    Should Not Be Empty    ${total_payment}
    Should Not Be Empty    ${total_interest}

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

Calculate EMI
    [Arguments]    ${principal}    ${monthly_rate}    ${months}
    ${principal_float}=    Convert To Number    ${principal}
    ${rate_float}=    Convert To Number    ${monthly_rate}
    ${months_int}=    Convert To Integer    ${months}
    
    ${emi}=    Run Keyword If    ${rate_float} == 0
    ...    Evaluate    ${principal_float} / ${months_int}
    ...    ELSE
    ...    Calculate EMI With Rate    ${principal_float}    ${rate_float}    ${months_int}
    
    [Return]    ${emi}

Calculate EMI With Rate
    [Arguments]    ${principal}    ${monthly_rate}    ${months}
    ${factor}=    Evaluate    (1 + ${monthly_rate}) ** ${months}
    ${emi}=    Evaluate    ${principal} * ${monthly_rate} * ${factor} / (${factor} - 1)
    [Return]    ${emi}

Calculate Total Payment
    [Arguments]    ${emi}    ${months}
    ${emi_float}=    Convert To Number    ${emi}
    ${months_int}=    Convert To Integer    ${months}
    ${total}=    Evaluate    ${emi_float} * ${months_int}
    [Return]    ${total}

Calculate Total Interest
    [Arguments]    ${total_payment}    ${principal}
    ${total_float}=    Convert To Number    ${total_payment}
    ${principal_float}=    Convert To Number    ${principal}
    ${interest}=    Evaluate    ${total_float} - ${principal_float}
    [Return]    ${interest}
