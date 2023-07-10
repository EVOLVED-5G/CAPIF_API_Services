*** Settings ***
Library           HttpLibrary

*** Test Cases ***
Example Test
    [Tags]        jms-not-working
    # Start the HTTP listener on port 8888
    Create Http Server    8888
    
    # Handle incoming requests using a keyword
    Handle Request    Handle Incoming Request
    
    # Stop the HTTP listener
    Stop Http Server
    
*** Keywords ***
Handle Incoming Request
    # Get the request data using the built-in keywords
    ${request_method}    Get Request Method
    ${request_body}    Get Request Body
    
    # Do something with the request data, such as logging it or saving it to a variable
    Log    Received HTTP request with method ${request_method} and body ${request_body}
