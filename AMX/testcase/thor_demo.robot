*** settings ***
Documentation     this test is a demo to
...               show add assert of thor command
...               if pass or not
Library           D:/robot_framwork/robot_demo/py_control_ns4.py
Library           MyTestLibrary

*** test cases ***
fwversion
    ${out}    command thor test    ?fwversion
    ${assertt}    set variable    [FWVERSION-SCALER_V1.06]
    log    ${out}
    should contain    ${out}    ${assertt}

VIDIN_AUTO_SELECT
    command thor test    VIDIN_AUTO_SELECT-disable
    ${out}    command thor test    ?VIDIN_AUTO_SELECT
    should contain    ${out}    VIDIN_AUTO_SELECT-DISABLE

VIDIN AUTO SELECT2
    command thor test    VIDIN_AUTO_SELECT-enable
    ${out}    command thor test    ?VIDIN_AUTO_SELECT
    should contain    ${out}    VIDIN_AUTO_SELECT-ENABLE

?vidin_status
    ${out}    command thor test    ?vidin_status
    should contain    ${out}    VIDIN_STATUS

CEC_DISP_POWER-ON
    ${out}    command thor test    CEC_DISP_POWER-ON
    should contain    ${out}    CEC_DISP_POWER-ON

CEC_DISP_POWER-OFF
    ${out}    command thor test    CEC_DISP_POWER-OFF
    should contain    ${out}    CEC_DISP_POWER-OFF

CEC_DISP_AUTO-ON
    ${EMPTY}    command thor test    CEC_DISP_AUTO-ON
    ${out}    command thor test    ?CEC_DISP_AUTO
    should contain    ${out}    CEC_DISP_AUTO-ON

CEC_DISP_AUTO-OFF
    ${EMPTY}    command thor test    CEC_DISP_AUTO-OFF
    ${out}    command thor test    ?CEC_DISP_AUTO
    should contain    ${out}    CEC_DISP_AUTO-OFF

ORDERED_SWITCH
    : FOR    ${in}    INRANGE    9
    \    For_two    ${in}

RANDOM_SWITCH
    : FOR    ${i}    IN RANGE    100
    \    ${in}    evaluate    random.randint(0,8)    random
    \    ${out}    generate    8
    \    command thor test    CI${in}O${out}

*** Keywords ***
EmbedLoop
    [Arguments]    @{lis}
    : FOR    ${abc}    IN    @{lis}
    \    log    embed:${abc}

For_two
    [Arguments]    ${input}
    ${result}    Run Keyword If    ${input}<=9    Set variable    9
    : FOR    ${output}    IN RANGE    ${result}
    \    command thor test    CI${input}O${output}

Generate_random
    [Arguments]    ${select}
    : FOR    ${i}    IN RANGE    ${select}
    \    ${out}    evaluate    random.randint(1,8)    random
    \    log    ${out}
