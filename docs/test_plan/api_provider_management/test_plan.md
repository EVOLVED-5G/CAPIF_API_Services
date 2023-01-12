[**[Return To All Test Plans]**]

- [Test Plan for CAPIF Api Provider Management](#test-plan-for-capif-api-provider-management)
- [Tests](#tests)
  - [Test Case 1: Register Api Provider](#test-case-1-register-api-provider)
  - [Test Case 2: Register Api Provider Already registered](#test-case-2-register-api-provider-already-registered)
  - [Test Case 3: Update Registered Api Provider](#test-case-3-update-registered-api-provider)
  - [Test Case 4: Update Not Registered Api Provider](#test-case-4-update-not-registered-api-provider)
  - [Test Case 5: Partially Update Registered Api Provider](#test-case-5-partially-update-registered-api-provider)
  - [Test Case 6: Partially Update Not Registered Api Provider](#test-case-6-partially-update-not-registered-api-provider)
  - [Test Case 7: Delete Registered Api Provider](#test-case-7-delete-registered-api-provider)
  - [Test Case 8: Delete Not Registered Api Provider](#test-case-8-delete-not-registered-api-provider)


# Test Plan for CAPIF Api Provider Management
At this documentation you will have all information and related files and examples of test plan for this API.

# Tests

## Test Case 1: Register Api Provider
* **Test ID**: ***capif_api_provider_management-1***
* **Description**:
  
  This test case will check that Api Provider can be registered con CCF by API Provider
* **Pre-Conditions**:
  
  * Provider is pre-authorised (has valid certificate from CAPIF Authority)

* **Information of Test**:

  1. Create public and private key at provider

  2. Register of Provider at CCF:
     * Send POST to *http://{CAPIF_HOSTNAME}:{CAPIF_HTTP_PORT}/register* 
     * body [provider register body]

  3. Register Provider at Provider Management:
     * Send POST *https://{CAPIF_HOSTNAME}/api-provider-management/v1/registrations*
     * body [provider request body]

* **Execution Steps**:
  
  1. Register Provider at CCF
  3. Register Provider at Provider Management
   
* **Expected Result**:

  1. Register Provider at Provider Management:
     1. **201 Created** response.
     2. body returned must accomplish **APIProviderEnrolmentDetails** data structure.
     3. Location Header must contain the new resource URL *{apiRoot}/api-provider-management/v1/registrations/{registrationId}*


## Test Case 2: Register Api Provider Already registered
* **Test ID**: ***capif_api_provider_management-2***
* **Description**:
  
  This test case will check that a Api Provider previously registered cannot be re-registered
* **Pre-Conditions**:
  
  * Api Provider was registered previously and there is a {registerId} for his Api Provider in the DB

* **Information of Test**:

  1. Create public and private key at provider

  2. Register of Provider at CCF:
     * Send POST to *http://{CAPIF_HOSTNAME}:{CAPIF_HTTP_PORT}/register* 
     * body [provider register body]

  3. Register Provider at Provider Management:
     * Send POST *https://{CAPIF_HOSTNAME}/api-provider-management/v1/registrations*
     * body [provider request body]

* **Execution Steps**:
  
  1. Register Provider at CCF
  3. Register Provider at Provider Management
  4. Re-Register Provider at Provider Management
   
* **Expected Result**:

  1. Re-Register Provider at Provider Management:
     1. **403 Forbidden** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status 403
        * title with message "Forbidden"
        * detail with message "Provider already registered".
        * cause with message "Identical provider reg sec".

## Test Case 3: Update Registered Api Provider  
* **Test ID**: ***capif_api_provider_management-3***
* **Description**:
  
  This test case will check that a Registered Api Provider can be updated
* **Pre-Conditions**:
  
  * Api Provider was registered previously and there is a {registerId} for his Api Provider in the DB

* **Information of Test**:

  1. Create public and private key at invoker

  2. Register of Provider at CCF:
     * Send POST to *http://{CAPIF_HOSTNAME}:{CAPIF_HTTP_PORT}/register* 
     * body [provider register body]

  3. Register Provider at Provider Management:
     * Send POST *https://{CAPIF_HOSTNAME}/api-provider-management/v1/registrations*
     * body [provider request body]
     * Get Resource URL from Location

  4. Update Provider at Provider Management:
     * Send PUT *https://{CAPIF_HOSTNAME}/api-provider-management/v1/registrations*
     * body [provider request body] with apiProvDomInfo set to ROBOT_TESTING_MOD


* **Execution Steps**:
  
  1. Register Provider at CCF
  2. Register Provider at Provider Management
  4. Re-Register Provider at Provider Management
   
* **Expected Result**:
  1. Register Provider at Provider Management:
     1. **201 Created** response.
     2. body returned must accomplish **APIProviderEnrolmentDetails** data structure.
     3. Location Header must contain the new resource URL *{apiRoot}/api-provider-management/v1/registrations/{registrationId}*


  2. Re-Register Provider at Provider Management:
     1. **200 OK** response.
     2. body returned must accomplish **APIProviderEnrolmentDetails** data structure, with:
        * apiProvDomInfo set to ROBOT_TESTING_MOD


## Test Case 4: Update Not Registered Api Provider 
* **Test ID**: ***capif_api_provider_management-4***
* **Description**:
  
  This test case will check that a Non-Registered Api Provider cannot be updated
* **Pre-Conditions**:
  
  * Api Provider was not registered previously

* **Information of Test**:

  1. Create public and private key at invoker

  2. Register of Provider at CCF:
     * Send POST to *http://{CAPIF_HOSTNAME}:{CAPIF_HTTP_PORT}/register* 
     * body [provider register body]

  3. Update Provider at Provider Management:
     * Send PUT *https://{CAPIF_HOSTNAME}/api-provider-management/v1/registrations*
     * body [provider request body]

* **Execution Steps**:
  
  1. Register Provider at CCF
  3. Update Provider at Provider Management
   
* **Expected Result**:

  1. Re-Register Provider at Provider Management:
     1. **404 Not Found** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status 404
        * title with message "Not Found"
        * detail with message "Not Exist Provider Enrolment Details".
        * cause with message "Not found registrations to send this api provider details".

## Test Case 5: Partially Update Registered Api Provider  
* **Test ID**: ***capif_api_provider_management-5***
* **Description**:
  
  This test case will check that a Registered Api Provider can be partially updated
* **Pre-Conditions**:
  
  * Api Provider was registered previously and there is a {registerId} for his Api Provider in the DB

* **Information of Test**:

  1. Create public and private key at invoker

  2. Register of Provider at CCF:
     * Send POST to *http://{CAPIF_HOSTNAME}:{CAPIF_HTTP_PORT}/register* 
     * body [provider register body]

  3. Register Provider at Provider Management:
     * Send POST *https://{CAPIF_HOSTNAME}/api-provider-management/v1/registrations*
     * body [provider request body]
     * Get resource from Location header

  4. Partial update provider at Provider Management:
     * Send PATCH *https://{CAPIF_HOSTNAME}/api-provider-management/v1/registrations/{registrationId}*
     * body [provider request patch body]

* **Execution Steps**:
  
  1. Register Provider at CCF
  2. Register Provider at Provider Management
  3. Partial update provider at Provider Management
   
* **Expected Result**:

  1. Partial update provider at Provider Management:
     1. **200 OK** response.
     2. body returned must accomplish **APIProviderEnrolmentDetails** data structure, with:
        * apiProvDomInfo with "ROBOT_TESTING_MOD"

## Test Case 6: Partially Update Not Registered Api Provider 
* **Test ID**: ***capif_api_provider_management-6***
* **Description**:
  
  This test case will check that a Non-Registered Api Provider cannot be partially updated  

* **Pre-Conditions**:
  
  * Api Provider was not registered previously

* **Information of Test**:

  1. Create public and private key at invoker

  2. Register of Provider at CCF:
     * Send POST to *http://{CAPIF_HOSTNAME}:{CAPIF_HTTP_PORT}/register* 
     * body [provider register body]

  3. Partial update Provider at Provider Management:
     * Send PATCH *https://{CAPIF_HOSTNAME}/api-provider-management/v1/registrations/{API_API_PROVIDER_NOT_REGISTERED}*
     * body [provider request patch body]
  

* **Execution Steps**:
  
  1. Register Provider at CCF
  2. Register Provider at Provider Management
  3. Partial update provider at Provider Management
   
* **Expected Result**:

  1. Partial update provider at Provider Management:
     1. **404 Not Found** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status 404
        * title with message "Not Found"
        * detail with message "Not Exist Provider Enrolment Details".
        * cause with message "Not found registrations to send this api provider details".

## Test Case 7: Delete Registered Api Provider   
* **Test ID**: ***capif_api_provider_management-7***
* **Description**:
  
  This test case will check that a Registered Api Provider can be deleted
* **Pre-Conditions**:
  
  * Api Provider was registered previously

* **Information of Test**:

  1. Create public and private key at provider

  2. Register of Provider at CCF:
     * Send POST to *http://{CAPIF_HOSTNAME}:{CAPIF_HTTP_PORT}/register* 
     * body [provider register body]

  3. Register Provider at Provider Management:
     * Send POST *https://{CAPIF_HOSTNAME}/api-provider-management/v1/registrations*
     * body [provider request body]
     * Get resource from Location header

  4. Delete registered provider at Provider Management:
     * Send DELETE *https://{CAPIF_HOSTNAME}/api-provider-management/v1/registrations/{registrationId}*

* **Execution Steps**:
  
  1. Register Provider at CCF
  2. Register Provider at Provider Management
  3. Delete Provider at Provider Management
   
* **Expected Result**:

  1. Delete Provider at Provider Management:
     1. **204 No Content** response.

## Test Case 8: Delete Not Registered Api Provider
* **Test ID**: ***capif_api_provider_management-8***
* **Description**:
  
  This test case will check that a Non-Registered Api Provider cannot be deleted
* **Pre-Conditions**:
  
  * Api Provider was not registered previously

* **Information of Test**:

  1. Create public and private key at provider

  2. Register of Provider at CCF:
     * Send POST to *http://{CAPIF_HOSTNAME}:{CAPIF_HTTP_PORT}/register* 
     * body [provider register body]

  3. Delete registered provider at Provider Management:
     * Send DELETE *https://{CAPIF_HOSTNAME}/api-provider-management/v1/registrations/{API_PROVIDER_NOT_REGISTERED}*

* **Execution Steps**:
  
  1. Register Provider at CCF
  2. Delete Provider at Provider Management
   
* **Expected Result**:

  1. Delete Provider at Provider Management:
     1. **404 Not Found** response.
     2. body returned must accomplish **ProblemDetails** data structure, with:
        * status 404
        * title with message "Not Found"
        * detail with message "Not Exist Provider Enrolment Details".
        * cause with message "Not found registrations to send this api provider details".


[provider request body]: ./provider_details_post_example.json  "API Provider Enrolment Request"

[provider request patch body]: ./provider_details_enrolment_details_patch_example.json  "API Provider Enrolment Patch Request"

[Return To All Test Plans]: ../README.md
