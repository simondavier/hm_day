*** settings ***
Documentation   sdfjewofjsofhsdflsdfjoejfslfds
...             sdfjsfoewfjoewifsvx,cvmxijfwoierjw
...             sfwei23u4e2093ru90fu0fjosdfw9eufwfuw0r
Library     ADD.py
*** test cases ***
testcase
    log   robot framework
variable
    ${a}  set variable  hello world
    log  ${a}
list
    ${abc}  create list     a  b  c
    log     ${abc}
catename
    ${hw}   catenate    hello world
    log     ${hw}
time
    ${t}    get time
    log     ${t}
    sleep   0.51
    log     ${t}
if
    ${a}    set variable    59
    run keyword if      ${a}>=90    log     优秀
    ...                 ELSE IF     ${a}>=70    log     良好
    ...                 ELSE IF     ${a}>=60    log     及格
    ...                 ELSE            log             不及格！
FOR
    :FOR    ${i}    IN RANGE    10
    \        log     ${i}
EVALUATEE
    ${d}    evaluate    random.randint(1000,9999)    random
    log     ${d}
    ${a}    set variable    1
    ${b}    set variable    1.0
    Should Not Be Equal As Numbers   ${a}    ${b}
keyword_study
    ${c}    add add     1       3
    ${d}    sub         3       3  
    ${e}    evaluate    int(0)
    log     ${c}
    should be equal     ${d}    ${e}

 
    
    
    
    