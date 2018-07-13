*** settings ***
Documentation   this is telnet demo 
...             data driven 
...               
Library     Telnet
Library     telnet_library_for_RF.py
#Test Setup  ${tn}   build connection    ${address1}    ${loginname}     ${password}
#Test Teardown   ${out2}     kill connection     ${tn}
#Test Template  send command and  verify 
*** variables ***
${address1}   192.168.1.100
${loginname}    test1
${password}     1111
${prompt}       \r\nLogin :
*** test cases ***
       
telnet1
#    [template]      send command and  verify
    [Setup]     set up keywords   
    #build connection    ${address1}    ${loginname}     ${password}
    ${out}  excut command       ${tn}   date
    log     ${out}
    [Teardown]   tear down keywords
    

    
*** keywords ***
#send command and verify
 #   [Arguments]    ${expression1}    ${expression2}   ${expected}
  #  command thor test     ${expression1}  
   # ${out}=     command thor test    ${expression2}
    #should contain    ${out}    ${expected}
set up keywords
    ${temp}=  build connection    ${address1}    ${loginname}     ${password}
    Set Test Variable   ${tn}   ${temp}
tear down keywords
    ${temp2}=   kill connection     ${tn}
    Set Test Variable   ${out2}   ${temp2}
    
    