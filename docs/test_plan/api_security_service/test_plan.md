[**[Return To All Test Plans]**]

- [Test Plan for CAPIF Api Security Service](#test-plan-for-capif-api-security-service)
- [Tests](#tests)
  - [Test Case 1: Create a security context for an API invoker](#test-case-1-create-a-security-context-for-an-api-invoker)
  - [Test Case 2: Create a security context for an API invoker with AEF entity role](#test-case-2-create-a-security-context-for-an-api-invoker-with-aef-entity-role)
  - [Test Case 3: Create a security context for an API invoker with AEF entity role and invalid apiInvokerId](#test-case-3-create-a-security-context-for-an-api-invoker-with-aef-entity-role-and-invalid-apiinvokerid)
  - [Test Case 4: Create a security context for an API invoker with Invoker entity role and invalid apiInvokerId](#test-case-4-create-a-security-context-for-an-api-invoker-with-invoker-entity-role-and-invalid-apiinvokerid)
  - [Test Case 5: Retrieve the Security Context of an API Invoker](#test-case-5-retrieve-the-security-context-of-an-api-invoker)
  - [Test Case 6: Retrieve the Security Context of an API Invoker with invalid apiInvokerID](#test-case-6-retrieve-the-security-context-of-an-api-invoker-with-invalid-apiinvokerid)
  - [Test Case 7: Retrieve the Security Context of an API Invoker with invalid apfId](#test-case-7-retrieve-the-security-context-of-an-api-invoker-with-invalid-apfid)
  - [Test Case 8: Delete the Security Context of an API Invoker](#test-case-8-delete-the-security-context-of-an-api-invoker)
  - [Test Case 9: Delete the Security Context of an API Invoker with Invoker entity role](#test-case-9-delete-the-security-context-of-an-api-invoker-with-invoker-entity-role)
  - [Test Case 10: Delete the Security Context of an API Invoker with Invoker entity role and invalid apiInvokerID](#test-case-10-delete-the-security-context-of-an-api-invoker-with-invoker-entity-role-and-invalid-apiinvokerid)
  - [Test Case 11: Delete the Security Context of an API Invoker with invalid apiInvokerID](#test-case-11-delete-the-security-context-of-an-api-invoker-with-invalid-apiinvokerid)
  - [Test Case 12: Update the Security Context of an API Invoker](#test-case-12-update-the-security-context-of-an-api-invoker)
  - [Test Case 13: Update the Security Context of an API Invoker with AEF entity role](#test-case-13-update-the-security-context-of-an-api-invoker-with-aef-entity-role)
  - [Test Case 14: Update the Security Context of an API Invoker with AEF entity role and invalid apiInvokerId](#test-case-14-update-the-security-context-of-an-api-invoker-with-aef-entity-role-and-invalid-apiinvokerid)
  - [Test Case 15: Update the Security Context of an API Invoker with invalid apiInvokerID](#test-case-15-update-the-security-context-of-an-api-invoker-with-invalid-apiinvokerid)
  - [Test Case 16: Revoke the authorization of the API invoker for APIs.](#test-case-16-revoke-the-authorization-of-the-api-invoker-for-apis)
  - [Test Case 17: Revoke the authorization of the API invoker for APIs without valid apfID.](#test-case-17-revoke-the-authorization-of-the-api-invoker-for-apis-without-valid-apfid)
  - [Test Case 18: Revoke the authorization of the API invoker for APIs with invalid apiInvokerId.](#test-case-18-revoke-the-authorization-of-the-api-invoker-for-apis-with-invalid-apiinvokerid)
  - [Test Case 19: Retrieve access token](#test-case-19-retrieve-access-token)
  - [Test Case 20: Retrieve access token with invalid apiInvokerId](#test-case-20-retrieve-access-token-with-invalid-apiinvokerid)
 


# Test Plan for CAPIF Api Security Service
At this documentation you will have all information and related files and examples of test plan for this API.

# Tests

## Test Case 1: Create a security context for an API invoker
  
  This test case will check that an API Invoker can create a Security context 

* Pre-Conditions: 
  
  API Invoker is pre-authorised (has valid apiInvokerID from CAPIF Authority) 

* Actions:

  PUT /trustedInvokers/{apiInvokerId}:
    
  Request Body: [service security body]

* Post-Conditions:
  
  Security Context for API Invoker is stored in CAPIF Database

  201 Successful created. 

  Security Context created sucessfully The URI of the created resource shall be returned in the "Location" HTTP header. 

  Location Contains the URI of the newly created resource, according to the structure: {apiRoot}/capif-security/v1/trustedInvokers/{apiInvokerId}

## Test Case 2: Create a security context for an API invoker with AEF entity role
  
  This test case will check that an API Exposure Function cannot create a Security context without valid apiInvokerID

* Pre-Conditions: 
  
  API Invoker is pre-authorised (has valid apiInvokerID), but user that create Security Context has AEF role

* Actions:

  PUT /trustedInvokers/{apiInvokerId}:
    
  Request Body: [service security body]

* Post-Conditions:
  
  Security Context for API Invoker is not stored in CAPIF Database

  403 Forbidden
## Test Case 3: Create a security context for an API invoker with AEF entity role and invalid apiInvokerId
  
  This test case will check that an API Exposure Function cannot create a Security context without valid apiInvokerID

* Pre-Conditions: 
  
  API Invoker is not pre-authorised (has invalid apiInvokerID) and user user that create Security Context has AEF role

* Actions:

  PUT /trustedInvokers/{apiInvokerId}:
    
  Request Body: [service security body]

* Post-Conditions:
  
  Security Context for API Invoker is not stored in CAPIF Database

  403 Forbidden 

## Test Case 4: Create a security context for an API invoker with Invoker entity role and invalid apiInvokerId
  
  This test case will check that an API Invoker cannot create a Security context without valid apiInvokerID

* Pre-Conditions: 
  
  API Invoker is not pre-authorised (has invalid apiInvokerID) 

* Actions:

  PUT /trustedInvokers/{apiInvokerId}:
    
  Request Body: [service security body]

* Post-Conditions:
  
  Security Context for API Invoker is not stored in CAPIF Database

  404 Not found
  
## Test Case 5: Retrieve the Security Context of an API Invoker
  
  This test case will check that an API Exposure Function can retrieve the Security context of an API Invoker

* Pre-Conditions: 
  
  API Exposure Function is pre-authorised (has valid apfId from CAPIF Authority) and API Invoker has created a valid Security Context

* Actions:

  GET /trustedInvokers/{apiInvokerId}:

* Post-Conditions:
  
  Security Context for API Invoker is returned from CAPIF Database

  200 The security related information of the API Invoker based on the request from the API exposing function.

## Test Case 6: Retrieve the Security Context of an API Invoker with invalid apiInvokerID
  
  This test case will check that an API Exposure Function cannot retrieve the Security context of an API Invoker without valid apiInvokerID

* Pre-Conditions: 
  
  API Exposure Function is pre-authorised (has valid apfId from CAPIF Authority) but API Invoker has not created a valid Security Context

* Actions:

  GET /trustedInvokers/{apiInvokerId}:
    
  Request Body: [service security body]

* Post-Conditions:
  
  Security Context is not found in CAPIF Database

  404 Not Found

## Test Case 7: Retrieve the Security Context of an API Invoker with invalid apfId
  
  This test case will check that an API Exposure Function cannot retrieve the Security context of an API Invoker without valid apfId

* Pre-Conditions: 
  
  API Exposure Function is not pre-authorised (has invalid apfId )

* Actions:

  GET /trustedInvokers/{apiInvokerId}:
    
  Request Body: [service security body]

* Post-Conditions:
  
  apfId is not found in CAPIF Database

  403 Forbidden

## Test Case 8: Delete the Security Context of an API Invoker
  
  This test case will check that an API Exposure Function can delete a Security context 

* Pre-Conditions: 
  
  API Exposure Function is pre-authorised (has valid apfID) 

* Actions:

  DELETE /trustedInvokers/{apiInvokerId}:
    
  Request Body: [service security body]

* Post-Conditions:
  
  Security Context for API Invoker is deleted in CAPIF Database

  204 No Content (Successful deletion of the existing subscription) 

## Test Case 9: Delete the Security Context of an API Invoker with Invoker entity role
  
  This test case will check that an API Invoker cannot delete a Security context

* Pre-Conditions: 
  
  API Invoker is pre-authorised (has valid apiInvokerID)

* Actions:

  DELETE /trustedInvokers/{apiInvokerId}:
    
  Request Body: [service security body]

* Post-Conditions:
  
  Security Context for API Invoker is not deleted in CAPIF Database

  403 Forbidden

## Test Case 10: Delete the Security Context of an API Invoker with Invoker entity role and invalid apiInvokerID
  
  This test case will check that an API Invoker cannot delete a Security context

* Pre-Conditions: 
  
  API Invoker is not pre-authorised (has invalid apiInvokerID)

* Actions:

  DELETE /trustedInvokers/{apiInvokerId}:
    
  Request Body: [service security body]

* Post-Conditions:
  
  Security Context for API Invoker is not deleted in CAPIF Database

  403 Forbidden

## Test Case 11: Delete the Security Context of an API Invoker with invalid apiInvokerID
  
  This test case will check that an API Exposure Function cannot delete a Security context of invalid apiInvokerId

* Pre-Conditions: 
  
  API Invoker is not pre-authorised (has invalid apiInvokerID)

* Actions:

  DELETE /trustedInvokers/{apiInvokerId}:
    
  Request Body: [service security body]

* Post-Conditions:
  
  Security Context for API Invoker is not deleted in CAPIF Database

  404 Forbidden

## Test Case 12: Update the Security Context of an API Invoker 
  
  This test case will check that an API Invoker can update a Security context 

* Pre-Conditions: 
  
  API Invoker is pre-authorised (has valid apiInvokerID from CAPIF Authority) 

* Actions:

  POST  /trustedInvokers/{apiInvokerId}/update: 
    
  Request Body: [service security body]

* Post-Conditions:
  
  Security Context for API Invoker is updated in CAPIF Database

  200 Successful updated.

Create a security context for an API invoker with Invoker entity role and invalid apiInvokerId

## Test Case 13: Update the Security Context of an API Invoker with AEF entity role
  
  This test case will check that an API Exposure Function cannot update a Security context

* Pre-Conditions: 
  
  API Invoker is pre-authorised (has valid apiInvokerID) 

* Actions:

  POST  /trustedInvokers/{apiInvokerId}/update: 
    
  Request Body: [service security body]

* Post-Conditions:
  
  Security Context for API Invoker is not updated in CAPIF Database

  403 Forbidden

## Test Case 14: Update the Security Context of an API Invoker with AEF entity role and invalid apiInvokerId
  
  This test case will check that an API Exposure Function cannot update a Security context

* Pre-Conditions: 
  
  API Invoker is not pre-authorised (has invalid apiInvokerID) 

* Actions:

  POST  /trustedInvokers/{apiInvokerId}/update: 
    
  Request Body: [service security body]

* Post-Conditions:
  
  Security Context for API Invoker is not updated in CAPIF Database

  403 Forbidden

## Test Case 15: Update the Security Context of an API Invoker with invalid apiInvokerID
  
  This test case will check that an API Invoker cannot update a Security context without valid apiInvokerId

* Pre-Conditions: 
  
  API Invoker is not pre-authorised (has invalid apiInvokerID) 

* Actions:

  POST  /trustedInvokers/{apiInvokerId}/update: 
    
  Request Body: [service security body]

* Post-Conditions:
  
  Security Context for API Invoker is not updated in CAPIF Database

  404 Not Found


## Test Case 16: Revoke the authorization of the API invoker for APIs.
  
  This test case will check that an API Exposure Function can revoke the authorization for APIs

* Pre-Conditions: 
  
  API Exposure Function is pre-authorised (has valid apfID) 

* Actions:

  POST  /trustedInvokers/{apiInvokerId}/delete: 
    
  Request Body: [security notification body]

* Post-Conditions:
  
  Security Context for API Invoker to access APIs of APIE Exposure Function is deleted in CAPIF Database

  204 Successful revoked.

## Test Case 17: Revoke the authorization of the API invoker for APIs without valid apfID.
  
  This test case will check that an API Exposure Function cannot revoke the authorization for APIs without valid apfId

* Pre-Conditions: 
  
  API Exposure Function is not pre-authorised (has invalid apfID) 

* Actions:

  POST  /trustedInvokers/{apiInvokerId}/delete: 
    
  Request Body: [security notification body]

* Post-Conditions:
  
  Security Context for API Invoker to access APIs of APIE Exposure Function is not deleted in CAPIF Database

  403 Forbidden

## Test Case 18: Revoke the authorization of the API invoker for APIs with invalid apiInvokerId.
  
  This test case will check that an API Exposure Function cannot revoke the authorization for APIs for invalid apiInvokerId

* Pre-Conditions: 
  
  API Exposure Function is  pre-authorised (has valid apfID) but apiIvokerId has no Security Context

* Actions:

  POST  /trustedInvokers/{apiInvokerId}/delete: 
    
  Request Body: [security notification body]

* Post-Conditions:
  
  Security Context for API Invoker to access APIs of APIE Exposure Function is not deleted in CAPIF Database

  404 Not Found

## Test Case 19: Retrieve access token
  
  This test case will check that an API Invoker can retrieve a security access token 

* Pre-Conditions: 
  
  API Invoker is pre-authorised (has valid apiInvokerId)

* Actions:

  POST /securities/{securityId}/token: //securityId will be the apiInvokerId
    
  Request Body: [access token req body]

* Post-Conditions:
  
  OAuth 2.0 access token is provided to API Invoker

  200 Successful Access Token Request

## Test Case 20: Retrieve access token with invalid apiInvokerId
  
  This test case will check that an API Invoker cannot retrieve a security access token without valid apiInvokerId

* Pre-Conditions: 
  
  API Invoker is not pre-authorised (has invalid apiInvokerId)

* Actions:

  POST /securities/{securityId}/token: //securityId will be the apiInvokerId
    
  Request Body: [access token req body]

* Post-Conditions:
  
  OAuth 2.0 access token is not provided to API Invoker

  403 Forbidden


  [Return To All Test Plans]: ../README.md



  [service security body]: ./service_security.json  "Service Security Request"
  [security notification body]: ./security_notification.json  "Security Notification Request"
  [access token req body]: ./access_token_req.json  "Access Token Request"