*** settings ***
Documentation   this is telnet demo 
...             data driven 
...               
Library     Telnet
Library     telnet_library_for_RF.py
Test Setup  set up keywords
Test Teardown  tear down keywords 
Test Template  templae keywords 
*** variables ***
${address1}   192.168.1.114  #${address1}   192.168.1.104 
${loginname}    test1
${password}     1111

*** test cases ***
       
telnet1
#    [template]      send command and  verify
    ${tn}       date      
    ${tn}       time
    ${tn}       cpu usage
    ${tn}       dns list
    ${tn}       get ip
    ${tn}       show mem
    ${tn}       show vs100 stats

    
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
templae keywords
    [Arguments]    ${expression1}    ${expression2}   
    ${out}=     excut command  ${expression1}  ${expression2}
    log        ${out}