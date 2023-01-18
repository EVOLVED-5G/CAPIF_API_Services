[**[Return To All Test Plans]**]

- [Test Plan for CAPIF Api Security Service](#test-plan-for-capif-api-security-service)
- [Tests](#tests)
  - [Test Case 1: Create a security context for an API invoker](#test-case-1-create-a-security-context-for-an-api-invoker)
  - [Test Case 2: Create a security context for an API invoker with Provider role](#test-case-2-create-a-security-context-for-an-api-invoker-with-provider-role)
  - [Test Case 3: Create a security context for an API invoker with Provider entity role and invalid apiInvokerId](#test-case-3-create-a-security-context-for-an-api-invoker-with-provider-entity-role-and-invalid-apiinvokerid)
  - [Test Case 4: Create a security context for an API invoker with Invoker entity role and invalid apiInvokerId](#test-case-4-create-a-security-context-for-an-api-invoker-with-invoker-entity-role-and-invalid-apiinvokerid)
  - [Test Case 5: Retrieve the Security Context of an API Invoker](#test-case-5-retrieve-the-security-context-of-an-api-invoker)
  - [Test Case 6: Retrieve the Security Context of an API Invoker with invalid apiInvokerID](#test-case-6-retrieve-the-security-context-of-an-api-invoker-with-invalid-apiinvokerid)
  - [Test Case 7: Retrieve the Security Context of an API Invoker with invalid apfId](#test-case-7-retrieve-the-security-context-of-an-api-invoker-with-invalid-apfid)
  - [Test Case 8: Delete the Security Context of an API Invoker](#test-case-8-delete-the-security-context-of-an-api-invoker)
  - [Test Case 9: Delete the Security Context of an API Invoker with Invoker entity role](#test-case-9-delete-the-security-context-of-an-api-invoker-with-invoker-entity-role)
  - [Test Case 10: Delete the Security Context of an API Invoker with Invoker entity role and invalid apiInvokerID](#test-case-10-delete-the-security-context-of-an-api-invoker-with-invoker-entity-role-and-invalid-apiinvokerid)
  - [Test Case 11: Delete the Security Context of an API Invoker with invalid apiInvokerID](#test-case-11-delete-the-security-context-of-an-api-invoker-with-invalid-apiinvokerid)
  - [Test Case 12: Update the Security Context of an API Invoker](#test-case-12-update-the-security-context-of-an-api-invoker)
  - [Test Case 13: Update the Security Context of an API Invoker with Provider entity role](#test-case-13-update-the-security-context-of-an-api-invoker-with-provider-entity-role)
  - [Test Case 14: Update the Security Context of an API Invoker with AEF entity role and invalid apiInvokerId](#test-case-14-update-the-security-context-of-an-api-invoker-with-aef-entity-role-and-invalid-apiinvokerid)
  - [Test Case 15: Update the Security Context of an API Invoker with invalid apiInvokerID](#test-case-15-update-the-security-context-of-an-api-invoker-with-invalid-apiinvokerid)
  - [Test Case 16: Revoke the authorization of the API invoker for APIs.](#test-case-16-revoke-the-authorization-of-the-api-invoker-for-apis)
  - [Test Case 17: Revoke the authorization of the API invoker for APIs without valid apfID.](#test-case-17-revoke-the-authorization-of-the-api-invoker-for-apis-without-valid-apfid)
  - [Test Case 18: Revoke the authorization of the API invoker for APIs with invalid apiInvokerId.](#test-case-18-revoke-the-authorization-of-the-api-invoker-for-apis-with-invalid-apiinvokerid)
  - [Test Case 19: Retrieve access token](#test-case-19-retrieve-access-token)
  - [Test Case 20: Retrieve access token by Provider](#test-case-20-retrieve-access-token-by-provider)
  - [Test Case 21: Retrieve access token by Provider with invalid apiInvokerId](#test-case-21-retrieve-access-token-by-provider-with-invalid-apiinvokerid)
  - [Test Case 22: Retrieve access token with invalid apiInvokerId](#test-case-22-retrieve-access-token-with-invalid-apiinvokerid)
  - [Test Case 23: Retrieve access token with invalid client\_id](#test-case-23-retrieve-access-token-with-invalid-client_id)
  - [Test Case 24: Retrieve access token with unsupported grant\_type](#test-case-24-retrieve-access-token-with-unsupported-grant_type)
  - [Test Case 25: Retrieve access token with invalid scope](#test-case-25-retrieve-access-token-with-invalid-scope)
  - [Test Case 26: Retrieve access token with invalid aefid at scope](#test-case-26-retrieve-access-token-with-invalid-aefid-at-scope)
  - [Test Case 27: Retrieve access token with invalid apiName at scope](#test-case-27-retrieve-access-token-with-invalid-apiname-at-scope)
 


# Test Plan for CAPIF Api Security Service
At this documentation you will have all information and related files and examples of test plan for this API.

# Tests

## Test Case 1: Create a security context for an API invoker
* **Test ID**: ***capif_security_api-1***
* **Description**:
  
  This test case will check that an API Invoker can create a Security context
* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerID from CAPIF Authority)

* **Information of Test**:
  1. Perform [Invoker Onboarding]
  2. Create Security Context for this Invoker
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Use Invoker Certificate

* **Execution Steps**:
  
  1. Register and onboard Invoker at CCF
  2. Store signed Certificate
  3. Create Security Context
   
* **Expected Result**:

  1. Create security context:
     1. **201 Created** response.
     2. body returned must accomplish **ServiceSecurity** data structure.
     3. Location Header must contain the new resource URL *{apiRoot}/capif-security/v1/trustedInvokers/{apiInvokerId}*


## Test Case 2: Create a security context for an API invoker with Provider role
* **Test ID**: ***capif_security_api-2***
* **Description**:
  
  This test case will check that an Provider cannot create a Security context with valid apiInvokerId.
* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerID), but user that create Security Context with Provider role

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Create Security Context for this Invoker but using Provider certificate.
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using AEF certificate

* **Execution Steps**:
  
  1. Register and onboard Invoker at CCF
  2. Register Provider at CCF
  3. Create Security Context using Provider certificate
   
* **Expected Result**:

  1. Create security context using Provider certificate:
     1. **401 Unauthorized** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **401**
        * title with message "Unauthorized"
        * detail with message "Role not authorized for this API route".
        * cause with message "User role must be invoker".

  2. No context stored at DB

## Test Case 3: Create a security context for an API invoker with Provider entity role and invalid apiInvokerId
* **Test ID**: ***capif_security_api-3***
* **Description**:

  This test case will check that an Provider cannot create a Security context with invalid apiInvokerID.
* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerID), but user that create Security Context with Provider role

* **Information of Test**:

  1. Perform [Provider Registration]

  2. Create Security Context for this not valid apiInvokerId and using Provider certificate.
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{API_INVOKER_NOT_VALID}*
     * body [service security body]
     * Using AEF certificate

* **Execution Steps**:
  
  1. Register Provider at CCF
  2. Create Security Context using Provider certificate
   
* **Expected Result**:

  1. Create security context using Provider certificate:
     1. **401 Unauthorized** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **401**
        * title with message "Unauthorized"
        * detail with message "Role not authorized for this API route".
        * cause with message "User role must be invoker".
  2. No context stored at DB

## Test Case 4: Create a security context for an API invoker with Invoker entity role and invalid apiInvokerId
* **Test ID**: ***capif_security_api-4***
* **Description**:
  
  This test case will check that an Invoker cannot create a Security context with valid apiInvokerId.
* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerID), but user that create Security Context with invalid apiInvokerId

* **Information of Test**:
  1. Perform [Invoker Onboarding]

  2. Create Security Context for this Invoker:
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{API_INVOKER_NOT_VALID}*
     * body [service security body]
     * Use Invoker Certificate

* **Execution Steps**:
  
  1. Register and onboard Invoker at CCF
  2. Create Security Context using Provider certificate
   
* **Expected Result**:

  1. Create security context using Provider certificate:
     1. **404 Not Found** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **404**
        * title with message "Not Found"
        * detail with message "Invoker not found".
        * cause with message "API Invoker not exists or invalid ID".

  2. No context stored at DB

  
## Test Case 5: Retrieve the Security Context of an API Invoker
* **Test ID**: ***capif_security_api-5***
* **Description**:
  
  This test case will check that an provider can retrieve the Security context of an API Invoker
* **Pre-Conditions**:
  
  * Provider is pre-authorised (has valid apfId from CAPIF Authority) and API Invoker has created a valid Security Context

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Create Security Context for this Invoker.
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker certificate

  3. Retrieve Security Context of Invoker by Provider:
     * Send GET *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * Using AEF Certificate

* **Execution Steps**:
  
  1. Register and onboard Invoker at CCF
  2. Register Provider at CCF
  3. Create Security Context using Provider certificate
  4. Retrieve Security Context by Provider
   
* **Expected Result**:
  1. Retrieve security context:
     1. **200 OK** response.
     2. body returned must accomplish **ServiceSecurity** data structure.


## Test Case 6: Retrieve the Security Context of an API Invoker with invalid apiInvokerID
* **Test ID**: ***capif_security_api-6***
* **Description**:
  
  This test case will check that an provider can retrieve the Security context of an API Invoker
* **Pre-Conditions**:
  
  * Provider is pre-authorised (has valid apfId from CAPIF Authority) and API Invoker has created a valid Security Context

* **Information of Test**:

  1. Perform [Provider Registration]

  2. Retrieve Security Context of invalid Invoker by Provider:
     * Send GET *https://{CAPIF_HOSTNAME}/trustedInvokers/{API_INVOKER_NOT_VALID}*
     * Using AEF Certificate.

* **Execution Steps**:
  
  2. Register Provider at CCF
  3. Create Security Context using Provider certificate
  4. Retrieve Security Context by Provider of invalid invoker
   
* **Expected Result**:
  1. Retrieve security context:
     1. **404 Not Found** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **404**
        * title with message "Not Found"
        * detail with message "Invoker not found".
        * cause with message "API Invoker not exists or invalid ID".


## Test Case 7: Retrieve the Security Context of an API Invoker with invalid apfId
* **Test ID**: ***capif_security_api-7***
* **Description**:
  
  This test case will check that an Provider cannot retrieve the Security context of an API Invoker without valid apfId
* **Pre-Conditions**:
  
  * API Exposure Function is not pre-authorised (has invalid apfId)

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Create Security Context for this Invoker
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate

  3. Retrieve Security Context as Invoker role:
     * Send GET *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * Using Invoker Certificate

* **Execution Steps**:
  
  1. Register and onboard Invoker at CCF
  2. Store signed Certificate
  3. Create Security Context
  4. Retrieve Security Context as Provider.
   
* **Expected Result**:

  1. Create security context:
     1. **401 Unauthorized** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **401**
        * title with message "Unauthorized"
        * detail with message "Role not authorized for this API route".
        * cause with message "User role must be aef".


## Test Case 8: Delete the Security Context of an API Invoker
* **Test ID**: ***capif_security_api-8***
* **Description**:
  
  This test case will check that an Provider can delete a Security context
* **Pre-Conditions**:
  
  * Provider is pre-authorised (has valid apfId from CAPIF Authority) and API Invoker has created a valid Security Context

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Create Security Context for this Invoker but using Provider certificate.
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using AEF certificate

  3. Delete Security Context of Invoker by Provider:
     * Send DELETE *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * Use AEF certificate

  4. Retrieve Security Context of Invoker by Provider:
     * Send GET *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * Using AEF Certificate

* **Execution Steps**:
  
  1. Register and onboard Invoker at CCF
  2. Register Provider at CCF
  3. Create Security Context using Provider certificate
  4. Delete Security Context by Provider
   
* **Expected Result**:

  1. Delete security context:
     1. **204 No Content** response.

  2. Retrieve security context:
     1. **404 Not Found** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **404**
        * title with message "Not Found"
        * detail with message "Security context not found".
        * cause with message "API Invoker not exists or invalid ID".


## Test Case 9: Delete the Security Context of an API Invoker with Invoker entity role
* **Test ID**: ***capif_security_api-9***
* **Description**:
  
  This test case will check that an Invoker cannot delete a Security context
* **Pre-Conditions**:
  
  * Provider is pre-authorised (has valid apfId from CAPIF Authority) and API Invoker has created a valid Security Context

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Create Security Context for this Invoker:
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker certificate

  3. Delete Security Context of Invoker:
     * Send DELETE *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * Use Invoker certificate

* **Execution Steps**:
  
  1. Register Provider at CCF
  2. Create Security Context using Provider certificate
  3. Delete Security Context by Invoker
   
* **Expected Result**:

  1. Delete security context:
     1. **401 Unauthorized** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **401**
        * title with message "Unauthorized"
        * detail with message "Role not authorized for this API route".
        * cause with message "User role must be aef".


## Test Case 10: Delete the Security Context of an API Invoker with Invoker entity role and invalid apiInvokerID
* **Test ID**: ***capif_security_api-10***
* **Description**:
  
  This test case will check that an Invoker cannot delete a Security context with invalid 
* **Pre-Conditions**:
  
  * Invoker is pre-authorised.

* **Information of Test**:

  1. Perform [Invoker Onboarding]

  2. Delete Security Context of Invoker:
     * Send DELETE *https://{CAPIF_HOSTNAME}/trustedInvokers/{API_INVOKER_NOT_VALID}*
     * Use Invoker certificate

* **Execution Steps**:
  
  1. Register Provider at CCF
  2. Delete Security Context by invoker
   
* **Expected Result**:

  1. Delete security context:
     1. **401 Unauthorized** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **401**
        * title with message "Unauthorized"
        * detail with message "Role not authorized for this API route".
        * cause with message "User role must be aef".


## Test Case 11: Delete the Security Context of an API Invoker with invalid apiInvokerID
* **Test ID**: ***capif_security_api-11***
* **Description**:
  
  This test case will check that an Provider cannot delete a Security context of invalid apiInvokerId
* **Pre-Conditions**:
  
  * Provider is pre-authorised (has valid apfId from CAPIF Authority).

* **Information of Test**:

  1. Perform [Provider Registration]

  2. Delete Security Context of Invoker by Provider:
     * Send DELETE *https://{CAPIF_HOSTNAME}/trustedInvokers/{API_INVOKER_NOT_VALID}*
     * Use AEF certificate

* **Execution Steps**:
  
  1. Register Provider at CCF
  2. Delete Security Context by provider
   
* **Expected Result**:

  1. Retrieve security context:
     1. **404 Not Found** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **404**
        * title with message "Not Found"
        * detail with message "Invoker not found".
        * cause with message "API Invoker not exists or invalid ID".


## Test Case 12: Update the Security Context of an API Invoker 
* **Test ID**: ***capif_security_api-12***
* **Description**:
  
  This test case will check that an API Invoker can update a Security context
* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerID from CAPIF Authority) and Provider is also authorized

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Create Security Context for this Invoker:
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate.
 
  3. Update Security Context of Invoker:
     * Send POST *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}/update*
     * body [service security body] but with notification destination modified to http://robot.testing2
     * Using Invoker Certificate.

  4. Retrieve Security Context of Invoker by Provider:
     * Send GET *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * Using AEF Certificate.

* **Execution Steps**:
  
  1. Register and onboard Invoker at CCF
  2. Register Provider at CCF
  3. Create Security Context By Invoker
  4. Update Security Context By Invoker
  5. Retrieve Security Context By Provider
   
* **Expected Result**:

  1. Update security context:
     1. **200 OK** response.
     2. body returned must accomplish **ServiceSecurity** data structure.
 
  2. Retrieve security context:
     1. **200 OK** response.
     2. body returned must accomplish **ServiceSecurity** data structure.
        1. Check is this returned object match with modified one.


## Test Case 13: Update the Security Context of an API Invoker with Provider entity role
* **Test ID**: ***capif_security_api-13***
* **Description**:
  
  This test case will check that an Provider cannot update a Security context

* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerID from CAPIF Authority) and Provider is also authorized.
  * Invoker has created the Security Context previously.

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Create Security Context for this Invoker:
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate.
 
  3. Update Security Context of Invoker by Provider:
     * Send POST *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}/update*
     * body [service security body] but with notification destination modified to http://robot.testing2
     * Using AEF Certificate

* **Execution Steps**:
  
  1. Register and onboard Invoker at CCF
  2. Register Provider at CCF
  3. Create Security Context
  4. Update Security Context as Provider
   
* **Expected Result**:

  1. Update security context:
     1. **401 Unauthorized** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **401**
        * title with message "Unauthorized"
        * detail with message "Role not authorized for this API route".
        * cause with message "User role must be invoker". 


## Test Case 14: Update the Security Context of an API Invoker with AEF entity role and invalid apiInvokerId
* **Test ID**: ***capif_security_api-14***
* **Description**:
  
  This test case will check that an Provider cannot update a Security context of invalid apiInvokerId

* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerID from CAPIF Authority) and Provider is also authorized.
  * Invoker has created the Security Context previously.

* **Information of Test**:

  1. Perform [Provider Registration]
 
  4. Update Security Context of Invoker by Provider:
     * Send POST *https://{CAPIF_HOSTNAME}/trustedInvokers/{API_INVOKER_NOT_VALID}/update*
     * body [service security body]
     * Using AEF Certificate

* **Execution Steps**:
  
  1. Register Provider at CCF
  2. Update Security Context as Provider
   
* **Expected Result**:

  1. Update security context:
     1. **401 Unauthorized** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **401**
        * title with message "Unauthorized"
        * detail with message "Role not authorized for this API route".
        * cause with message "User role must be invoker". 


## Test Case 15: Update the Security Context of an API Invoker with invalid apiInvokerID
* **Test ID**: ***capif_security_api-15***
* **Description**:
  
  This test case will check that an API Invoker cannot update a Security context not valid apiInvokerId
* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerID from CAPIF Authority)

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]
 
  2. Update Security Context of Invoker:
     * Send POST *https://{CAPIF_HOSTNAME}/trustedInvokers/{API_INVOKER_NOT_VALID}/update*
     * body [service security body]
     * Using Invoker Certificate.

* **Execution Steps**:
  
  1. Register and onboard Invoker at CCF
  2. Update Security Context
   
* **Expected Result**:

1. Retrieve security context:
     1. **404 Not Found** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **404**
        * title with message "Not Found"
        * detail with message "Invoker not found".
        * cause with message "API Invoker not exists or invalid ID".


## Test Case 16: Revoke the authorization of the API invoker for APIs.
* **Test ID**: ***capif_security_api-16***
* **Description**:
  
  This test case will check that a Provider can revoke the authorization for APIs

* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerID from CAPIF Authority) and Provider is also authorized

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Create Security Context By Invoker:
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate
 
  3. Revoke Authorization by Provider:
     * Send POST *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}/delete*
     * body [security notification body]
     * Using AEF Certificate.

  4. Retrieve Security Context by Provider:
     * Send GET *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * Using AEF Certificate.


* **Execution Steps**:
  
  1. Register and onboard Invoker at CCF
  2. Register Provider at CCF
  3. Create Security Context by Invoker
  4. Revoke Security Context by Provider
  5. Retrieve Security Context by Provider
   
* **Expected Result**:

  1. Revoke Authorization:
     1. **204 No Content** response.

  2. Retrieve security context:
     1. **404 Not Found** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **404**
        * title with message "Not Found"
        * detail with message "Security context not found".
        * cause with message "API Invoker has no security context".


## Test Case 17: Revoke the authorization of the API invoker for APIs without valid apfID.
* **Test ID**: ***capif_security_api-17***
* **Description**:
  
  This test case will check that an Invoker can't revoke the authorization for APIs

* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerID from CAPIF Authority) and Provider is also authorized

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Create Security Context for this Invoker:
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate.
 
  3. Revoke Authorization by invoker:
     * Send POST *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}/delete*
     * body [security notification body]
     * Using Invoker Certificate

  4. Retrieve Security Context of Invoker by Provider:
     * Send GET *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * Using Provider Certificate

* **Execution Steps**:
  
  1. Register and onboard Invoker at CCF
  2. Register Provider at CCF
  3. Create Security Context
  4. Revoke Security Context by invoker
  5. Retrieve Security Context
   
* **Expected Result**:

  1. Revoke Security Context by invoker:
     1. **401 Unauthorized** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **401**
        * title with message "Unauthorized"
        * detail with message "Role not authorized for this API route".
        * cause with message "User role must be provider". 

  3. Retrieve security context:
     1. **200 OK** response.
     2. body returned must accomplish **ServiceSecurity** data structure.
        1. Check is this returned object match with created one.


## Test Case 18: Revoke the authorization of the API invoker for APIs with invalid apiInvokerId.
* **Test ID**: ***capif_security_api-18***
* **Description**:
  
  This test case will check that an API Exposure Function cannot revoke the authorization for APIs for invalid apiInvokerId

* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerID from CAPIF Authority) and Provider is also authorized

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Create Security Context for this Invoker:
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate.
 
  3. Revoke Authorization by Provider:
     * Send POST *https://{CAPIF_HOSTNAME}/trustedInvokers/{API_INVOKER_NOT_VALID}/delete*
     * body [security notification body]
     * Using AEF Certificate.

  4. Retrieve Security Context of Invoker by Provider:
     * Send GET *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}?authenticationInfo=true&authorizationInfo=true*
     * This request will ask with parameter to retrieve authenticationInfo and authorizationInfo
     * Using AEF Certificate.

* **Execution Steps**:
  
  1. Register and onboard Invoker at CCF
  2. Register Provider at CCF
  3. Create Security Context
  4. Revoke Security Context by Provider
  5. Retrieve Security Context
   
* **Expected Result**:

  1. Revoke Security Context by invoker:
     1. **404 Not Found** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status **404**
        * title with message "Not Found"
        * detail with message "Invoker not found".
        * cause with message "API Invoker not exists or invalid ID".

  3. Retrieve security context:
     1. **200 OK** response.
     2. body returned must accomplish **ServiceSecurity** data structure.
        1. Check is this return one object that match with created one.


## Test Case 19: Retrieve access token
* **Test ID**: ***capif_security_api-19***
* **Description**:
  
  This test case will check that an API Invoker can retrieve a security access token OAuth 2.0.
* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerId)
  * Service API of Provider is published

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_1
     * Use APF Certificate

  3. Request Discover Published APIs not filtered:
     * Send GET to ccf_discover_url *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}*
     * Param api-invoker-id is mandatory
     * Using invoker certificate

  4. Create Security Context for this Invoker
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate.
     * Create Security Information Body with one **securityInfo** for each aef present at each serviceAPIDescription present at Discover.

  5. Request Access Token by invoker:
     * Sent POST *https://{CAPIF_HOSTNAME}/securities/{securityId}/token*:
     * body [access token req body] and example [example]
       * ***securityId*** is apiInvokerId.
       * ***grant_type=client_credentials***.
       * Create Scope properly for request: ***3gpp#{aef_id}:{api_name}***
     * Using Invoker Certificate.
  
* **Execution Steps**:
  
  1. Register Provider at CCF, store certificates and Publish Service API service_1 at CCF
  2. Register and onboard Invoker at CCF
  3. Discover Service APIs by Invoker.
  4. Create Security Context According to Service APIs discovered.
  5. Request Access Token
   
* **Expected Result**:

  1. Response to Request of Access Token:
     1. **200 OK**
     2. body must follow **AccessTokenRsp** with:
        1. access_token present
        2. token_type=Bearer

## Test Case 20: Retrieve access token by Provider
* **Test ID**: ***capif_security_api-20***
* **Description**:
  
  This test case will check that an API Exposure Function cannot revoke the authorization for APIs for invalid apiInvokerId

* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerID from CAPIF Authority) and Provider is also authorized

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_1
     * Use APF Certificate

  3. Request Discover Published APIs not filtered:
     * Send GET to ccf_discover_url *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}*
     * Param api-invoker-id is mandatory
     * Using invoker certificate

  4. Create Security Context for this Invoker
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate.
     * Create Security Information Body with one **securityInfo** for each aef present at each serviceAPIDescription present at Discover.

  5. Request Access Token by provider:
     * Sent POST *https://{CAPIF_HOSTNAME}/securities/{securityId}/token*:
     * body [access token req body]
       * ***securityId*** is apiInvokerId
       * ***grant_type=client_credentials***
     * Using AEF certificate

* **Execution Steps**:
  1. Register Provider at CCF, store certificates and Publish Service API service_1 at CCF
  2. Register and onboard Invoker at CCF
  3. Discover Service APIs by Invoker.
  4. Create Security Context According to Service APIs discovered.
  5. Request Access Token by Provider
   
* **Expected Result**:

  1. Response to Request of Access Token:
     1. **401 Unauthorized** response.
     2. body returned must accomplish **AccessTokenErr** data structure, with:
        * error unauthorized_client
        * error_description=Role not authorized for this API route

## Test Case 21: Retrieve access token by Provider with invalid apiInvokerId
* **Test ID**: ***capif_security_api-21***
* **Description**:
  
  This test case will check that an API Exposure Function cannot retrieve a security access token without valid apiInvokerId

* **Pre-Conditions**:
  
  * API Invoker is pre-authorised and Provider is also authorized


* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_1
     * Use APF Certificate

  3. Request Discover Published APIs not filtered:
     * Send GET to ccf_discover_url *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}*
     * Param api-invoker-id is mandatory
     * Using invoker certificate

  4. Create Security Context for this Invoker
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate.
     * Create Security Information Body with one **securityInfo** for each aef present at each serviceAPIDescription present at Discover.

  5. Request Access Token by provider:
     * Sent POST *https://{CAPIF_HOSTNAME}/securities/{API_INVOKER_NOT_VALID}/token*.
     * body [access token req body]
       * ***securityId*** is apiInvokerId
       * ***grant_type=client_credentials***
     * Using AEF certificate

* **Execution Steps**:
  1. Register Provider at CCF, store certificates and Publish Service API service_1 at CCF
  2. Register and onboard Invoker at CCF
  3. Discover Service APIs by Invoker.
  4. Create Security Context According to Service APIs discovered.
  5. Request Access Token by Provider
   
* **Expected Result**:

  1. Response to Request of Access Token:
     1. **401 Unauthorized** response.
     2. body returned must accomplish **AccessTokenErr** data structure, with:
        * error unauthorized_client
        * error_description=Role not authorized for this API route
   

## Test Case 22: Retrieve access token with invalid apiInvokerId
* **Test ID**: ***capif_security_api-22***
* **Description**:
  
  This test case will check that an API Invoker can't retrieve a security access token without valid apiInvokerId

* **Pre-Conditions**:
  
  * API Invoker is pre-authorised (has valid apiInvokerId)

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]
  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_1
     * Use APF Certificate
  3. Request Discover Published APIs not filtered:
     * Send GET to ccf_discover_url *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}*
     * Param api-invoker-id is mandatory
     * Using invoker certificate
  4. Create Security Context for this Invoker
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate.
     * Create Security Information Body with one **securityInfo** for each aef present at each serviceAPIDescription present at Discover.
  5. Request Access Token by invoker:
     * Sent POST *https://{CAPIF_HOSTNAME}/securities/{API_INVOKER_NOT_VALID}/token*.
     * body [access token req body]
       * ***securityId*** is apiInvokerId
       * ***grant_type=client_credentials***
     * Using Invoker certificate

* **Execution Steps**:
  1. Register Provider at CCF, store certificates and Publish Service API service_1 at CCF
  2. Register and onboard Invoker at CCF
  3. Discover Service APIs by Invoker.
  4. Create Security Context According to Service APIs discovered.
  5. Request Access Token by Invoker

* **Expected Result**:

  1. Response to Request of Access Token:
     1. **404 Not Found** response.
     2. body returned must accomplish **ProblemDetails29571** data structure, with:
        * status 404
        * title Not Found
        * detail Security context not found
        * cause API Invoker has no security context


**NOTE: ProblemDetails29571 is the definition present for this request at swagger of ProblemDetails, and this is different from definition of ProblemDetails across other CAPIF Services**

## Test Case 23: Retrieve access token with invalid client_id
* **Test ID**: ***capif_security_api-23***
* **Description**:
  
  This test case will check that an API Exposure Function cannot retrieve a security access token without valid client_id at body

* **Pre-Conditions**:
  
  * API Invoker is pre-authorised and Provider is also authorized

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_1
     * Use APF Certificate

  3. Request Discover Published APIs not filtered:
     * Send GET to ccf_discover_url *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}*
     * Param api-invoker-id is mandatory
     * Using invoker certificate

  4. Create Security Context for this Invoker
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate.
     * Create Security Information Body with one **securityInfo** for each aef present at each serviceAPIDescription present at Discover.

  5. Request Access Token by invoker:
     * Sent POST *https://{CAPIF_HOSTNAME}/securities/{securityId}/token*.
     * body [access token req body]
       * ***securityId*** is apiInvokerId
       * ***grant_type=client_credentials***
       * **client_id is not-valid** 
     * Using Invoker certificate

* **Execution Steps**:
  1. Register Provider at CCF, store certificates and Publish Service API service_1 at CCF
  2. Register and onboard Invoker at CCF
  3. Discover Service APIs by Invoker.
  4. Create Security Context According to Service APIs discovered.
  5. Request Access Token by Invoker
   
* **Expected Result**:

  1. Response to Request of Access Token:
     1. **400 Bad Request** response.
     2. body returned must accomplish **AccessTokenErr** data structure, with:
        * error invalid_client
        * error_description=Client Id not found


## Test Case 24: Retrieve access token with unsupported grant_type
* **Test ID**: ***capif_security_api-24***
* **Description**:
  
  This test case will check that an API Exposure Function cannot retrieve a security access token with unsupported grant_type

* **Pre-Conditions**:
  
  * API Invoker is pre-authorised and Provider is also authorized

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]
   
  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_1
     * Use APF Certificate

  3. Request Discover Published APIs not filtered:
     * Send GET to ccf_discover_url *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}*
     * Param api-invoker-id is mandatory
     * Using invoker certificate

  4. Create Security Context for this Invoker
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate.
     * Create Security Information Body with one **securityInfo** for each aef present at each serviceAPIDescription present at Discover.

  5. Request Access Token by invoker:
     * Sent POST *https://{CAPIF_HOSTNAME}/securities/{securityId}/token*.
     * body [access token req body]
       * ***securityId*** is apiInvokerId
       * ***grant_type=not_valid***
     * Using Invoker certificate

* **Execution Steps**:
  1. Register Provider at CCF, store certificates and Publish Service API service_1 at CCF
  2. Register and onboard Invoker at CCF
  3. Discover Service APIs by Invoker.
  4. Create Security Context According to Service APIs discovered.
  5. Request Access Token by Invoker
   
* **Expected Result**:

  1. Response to Request of Access Token:
     1. **400 Bad Request** response.
     2. body returned must accomplish **AccessTokenErr** data structure, with:
        * error unsupported_grant_type
        * error_description=Invalid value for `grant_type` \\(${grant_type}\\), must be one of \\['client_credentials'\\] - 'grant_type'

## Test Case 25: Retrieve access token with invalid scope
* **Test ID**: ***capif_security_api-25***
* **Description**:
  
  This test case will check that an API Exposure Function cannot retrieve a security access token with complete invalid scope

* **Pre-Conditions**:
  
  * API Invoker is pre-authorised and Provider is also authorized

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_1
     * Use APF Certificate

  3. Request Discover Published APIs not filtered:
     * Send GET to ccf_discover_url *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}*
     * Param api-invoker-id is mandatory
     * Using invoker certificate

  4. Create Security Context for this Invoker
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate.
     * Create Security Information Body with one **securityInfo** for each aef present at each serviceAPIDescription present at Discover.

  5. Request Access Token by invoker:
     * Sent POST *https://{CAPIF_HOSTNAME}/securities/{securityId}/token*.
     * body [access token req body]
       * ***securityId*** is apiInvokerId
       * ***grant_type=client_credentials***
       * ***scope=not-valid-scope***
     * Using Invoker certificate

* **Execution Steps**:
  1. Register Provider at CCF, store certificates and Publish Service API service_1 at CCF
  2. Register and onboard Invoker at CCF
  3. Discover Service APIs by Invoker.
  4. Create Security Context According to Service APIs discovered.
  5. Request Access Token by Invoker
   
* **Expected Result**:

  1. Response to Request of Access Token:
     1. **400 Bad Request** response.
     2. body returned must accomplish **AccessTokenErr** data structure, with:
        * error invalid_scope
        * error_description=The first characters must be '3gpp'


## Test Case 26: Retrieve access token with invalid aefid at scope
* **Test ID**: ***capif_security_api-26***
* **Description**:
  
  This test case will check that an API Exposure Function cannot retrieve a security access token with invalid aefId at scope

* **Pre-Conditions**:
  
  * API Invoker is pre-authorised and Provider is also authorized

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_1
     * Use APF Certificate

  3. Request Discover Published APIs not filtered:
     * Send GET to ccf_discover_url *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}*
     * Param api-invoker-id is mandatory
     * Using invoker certificate

  4. Create Security Context for this Invoker
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate.
     * Create Security Information Body with one **securityInfo** for each aef present at each serviceAPIDescription present at Discover.

  5. Request Access Token by invoker:
     * Sent POST *https://{CAPIF_HOSTNAME}/securities/{securityId}/token*.
     * body [access token req body]
       * ***securityId*** is apiInvokerId
       * ***grant_type=client_credentials***
       * ***scope=3gpp#1234:service_1***
     * Using Invoker certificate

* **Execution Steps**:
  1. Register Provider at CCF, store certificates and Publish Service API service_1 at CCF
  2. Register and onboard Invoker at CCF
  3. Discover Service APIs by Invoker.
  4. Create Security Context According to Service APIs discovered.
  5. Request Access Token by Invoker
   
* **Expected Result**:

  1. Response to Request of Access Token:
     1. **400 Bad Request** response.
     2. body returned must accomplish **AccessTokenErr** data structure, with:
        * error invalid_scope
        * error_description=One of aef_id not belongs of your security context


## Test Case 27: Retrieve access token with invalid apiName at scope
* **Test ID**: ***capif_security_api-27***
* **Description**:
  
  This test case will check that an API Exposure Function cannot retrieve a security access token with invalid apiName at scope

* **Pre-Conditions**:
  
  * API Invoker is pre-authorised and Provider is also authorized

* **Information of Test**:

  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_1
     * Use APF Certificate

  3. Request Discover Published APIs not filtered:
     * Send GET to ccf_discover_url *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}*
     * Param api-invoker-id is mandatory
     * Using invoker certificate

  4. Create Security Context for this Invoker
     * Send PUT *https://{CAPIF_HOSTNAME}/trustedInvokers/{apiInvokerId}*
     * body [service security body]
     * Using Invoker Certificate.
     * Create Security Information Body with one **securityInfo** for each aef present at each serviceAPIDescription present at Discover.

  5. Request Access Token by invoker:
     * Sent POST *https://{CAPIF_HOSTNAME}/securities/{securityId}/token*.
     * body [access token req body]
       * ***securityId*** is apiInvokerId
       * ***grant_type=client_credentials***
       * ***scope=3gpp#{aef_id}:not-valid***
     * Using Invoker certificate

* **Execution Steps**:
  1. Register Provider at CCF, store certificates and Publish Service API service_1 at CCF
  2. Register and onboard Invoker at CCF
  3. Discover Service APIs by Invoker.
  4. Create Security Context According to Service APIs discovered.
  5. Request Access Token by Invoker
   
* **Expected Result**:

  1. Response to Request of Access Token:
     1. **400 Bad Request** response.
     2. body returned must accomplish **AccessTokenErr** data structure, with:
        * error invalid_scope
        * error_description=One of the api names does not exist or is not associated with the aef id provided


  [Return To All Test Plans]: ../README.md



  [service security body]: ./service_security.json  "Service Security Request"
  [security notification body]: ./security_notification.json  "Security Notification Request"
  [access token req body]: ./access_token_req.json  "Access Token Request"
  [example]: ./access_token_req.json  "Access Token Request Example"

  [invoker onboarding]: ../common_operations/README.md#register-an-invoker "Invoker Onboarding"
  [provider registration]: ../common_operations/README.md#register-a-provider "Provider Registration"


