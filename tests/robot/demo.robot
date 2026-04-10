*** Settings ***
Library    OperatingSystem

*** Test Cases ***
Robot Demo - Basic Check
    Log    Hello from Robot Framework
    Should Be Equal    2    2
