*** Settings ***

Library         String
Library         HttpCtrl.Client
Library         HttpCtrl.Server

Test Setup       Initialize HTTP Client And Server
Test Teardown    Terminate HTTP Server

*** Test Cases ***

Receive And Reply To POST
    [Tags]   jms
    # ${request body}=   Set Variable   { "method": "POST" }
    # Send HTTP Request Async   POST   /post   ${request body}

    Wait For Request  300
    Reply By   200

    # ${method}=   Get Request Method
    # ${url}=      Get Request Url
    # ${body}=     Get Request Body
    # ${body}=     Decode Bytes To String   ${body}   UTF-8

    # Should Be Equal   ${method}   POST
    # Should Be Equal   ${url}      /post
    # Should Be Equal   ${body}     ${request body}

*** Keywords ***

Initialize HTTP Client And Server
    # Initialize Client   127.0.0.1   8000
    Start Server        127.0.0.1   8000

Terminate HTTP Server
    Stop Server