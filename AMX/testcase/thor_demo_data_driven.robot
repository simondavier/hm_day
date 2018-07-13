*** settings ***
Documentation   this test is a demo to 
...             show add assert of thor command 
...             if pass or not
Library     D:/robot_framwork/robot_demo/py_control_ns4.py
Test Template  send command and  verify 
*** test cases ***


CEC_DISP_AUTO-ON
#    [template]      send command and  verify
#    CEC_DISP_AUTO-ON    ?CEC_DISP_AUTO      CEC_DISP_AUTO-ON
#    CEC_DISP_AUTO-OFF    ?CEC_DISP_AUTO      CEC_DISP_AUTO-OFF
     FP_LOCKOUT-DISABLE     ?FP_LOCKOUT        FP_LOCKOUT-DISABLE
    ?FWVERSION              ?FWVERSION         FWVERSION-STM32_V1.3 
    
*** keywords ***
send command and verify
    [Arguments]    ${expression1}    ${expression2}   ${expected}
    command thor test     ${expression1}  
    ${out}=     command thor test    ${expression2}
    should contain    ${out}    ${expected}
    
    