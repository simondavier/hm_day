*** Settings ***
Suite Setup       Setup_pre_config
Library           ../../../hm_day/AMX/source/MyTestLibrary/icsp_module.py

*** Test Cases ***
001_Order_switch
    [Documentation]    Test Summary: This case will switch all ports by ordered.
    ...
    ...    Test Step:
    ...    1. Reset all ports;
    ...    2. Create a matrix to record current status;
    ...    3. Send thor command to switch port;
    ...    4. Check and Compare the matrix after set;
    ...    5. Return True if pass.
    ...
    ...    Test Target: All switch can be pass.
    ...
    ...    Comments:
    ...    1. Master sometimes can not get the result;
    ...    2. This test should last 2 hours after init running.
    ${res}    Icsp Order Switch    8    8
    Should Be Equal    ${res}    True

002_Random_switch
    [Documentation]    Test Summary: This case will switch all ports by random.
    ...
    ...    Test Step:
    ...    1. Reset all ports;
    ...    2. Create a random input;
    ...    3. Create a random output;
    ...    2. Create a matrix to record status;
    ...    3. Send thor command to switch port;
    ...    4. Check and Compare the matrix after set;
    ...    5. Return True if pass.
    ...
    ...    Test Target: All switch can be pass.
    ...
    ...    Comments:
    ...    1. Master sometimes can not get the result;
    ...    2. This test time will be last according to execute times.
    ${res}    Random Switch    8    8    1000
    Should Be Equal    ${res}    True

*** Keywords ***
Setup_pre_config
    log    test begin:
    Open Thor Command    00-60-9f-a4-5f-ae    00-60-9f-a4-0e-a9
    sleep    5
