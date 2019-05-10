*** Settings ***
Metadata        Log File    [.|${CURDIR}/result]

Library         REST  ssl_verify=false
Library         Collections
Library         BuiltIn

Variables       ${CURDIR}/config/testcase.yaml


*** Variables ***


*** Test Cases ***
1. list
   REST.Expect Response    ${CURDIR}/json/response_list.json
   REST.Get    ${url}/tasks
   REST.Output    request
   REST.Output    response
   REST.Integer    response status    200

2. post
   &{reqbody}=    REST.Input    ${CURDIR}/json/request_post.json
   REST.Expect Response    ${CURDIR}/json/response_single.json
   &{res}    REST.Post    ${url}/tasks    ${reqbody}
   REST.Output    request
   REST.Output    response
   REST.Integer    response status    201

   Output    response
   Set Suite Variable    ${taskid}    ${res.body.id}

3. get created item
   REST.Expect Response    ${CURDIR}/json/response_single.json
   REST.Get    ${url}/tasks/${taskid}
   REST.Output    request
   REST.Output    response
   REST.Integer    response status    200

4. list again
   REST.Expect Response    ${CURDIR}/json/response_list.json
   REST.Get    ${url}/tasks
   REST.Output    request
   REST.Output    response
   REST.Integer    response status    200

5. put
   &{reqbody}=    REST.Input    ${CURDIR}/json/request_put.json
   REST.Expect Response    ${CURDIR}/json/response_single.json
   REST.Put    ${url}/tasks/${taskid}    ${reqbody}
   REST.Output    request
   REST.Output    response
   REST.Integer    response status    200

6. delete
   REST.Delete    ${url}/tasks/${taskid}    validate=False
   REST.Output    request
   REST.Integer    response status    204

7. get removed item (expecting error)
   REST.Expect Response    ${CURDIR}/json/error.json
   REST.Get    ${url}/tasks/${taskid}
   REST.Output    request
   REST.Output    response
   REST.Integer    response status    404


# *** keywords ***
# Check Attribute Value Post Subscriber
#    [Arguments]    ${baseJson}
#    &{request}=    Copy Dictionary    ${baseJson}
