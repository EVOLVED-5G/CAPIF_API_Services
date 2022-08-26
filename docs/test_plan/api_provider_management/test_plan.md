[**[Return To All Test Plans]**]

- [Test Plan for CAPIF Api Provider Management](#test-plan-for-capif-api-provider-management)
- [Tests](#tests)
  - [Test Case 1: Register Api Provider](#test-case-1-register-api-provider)
  - [Test Case 2: Register Api Provider Already registered](#test-case-2-register-api-provider-already-registered)
  - [Test Case 3: Update Registered Api Provider](#test-case-3-update-registered-api-provider)
  - [Test Case 4: Update Not Registered Api Provider](#test-case-4-update-not-registered-api-provider)
  - [Test Case 5: Partially Update Registered Api Provider](#test-case-5-update-not-registered-api-provider)
  - [Test Case 6: Partially Update Not Registered Api Provider](#test-case-6-update-not-registered-api-provider)
  - [Test Case 7: Delete Registered Api Provider](#test-case-7-delete-registered-api-provider)
  - [Test Case 8: Delete Not Registered Api Provider](#test-case-8-delete-not-registered-api-provider)


# Test Plan for CAPIF Api Provider Management
At this documentation you will have all information and related files and examples of test plan for this API.

# Tests

## Test Case 1: Register Api Provider
  
  This test case will check that Api Provider can be registered 

* Pre-Conditions:
  
  Api Provider was not registered previously.

* Actions:

  Register Api Provider
  
  Request Body: [request body]

* Post-Conditions:
  
  201 API invoker on-boarded successfully.

  Header Location at response contains the URI of the newly created resource, according to the structure: {apiRoot}/api-provider-management/v1/onboardedInvokers/{registerId}


## Test Case 2: Register Api Provider Already registered
  
  This test case will check that a Api Provider previously registered canot be re-registered

* Pre-Conditions:
  
  Api Provider was registered previously and there is a {registerId} for his Api Provider in the DB

* Actions:

  Register Api Provider
  
  Request Body: [request body]

* Post-Conditions:
  
  403 Forbidden returned.

## Test Case 3: Update Registered Api Provider  
  
  This test case will check that a Registered Api Provider can be updated  

* Pre-Conditions:
  
  Api Provider was registered previously and there is a {registerId} for his Api Provider in the DB

* Actions:

  Update Api Provider onboardingDetails
  
  Request Body: [request body]

* Post-Conditions:
  
  200 API invoker details updated successfully.

## Test Case 4: Update Not Registered Api Provider 
  
  This test case will check that a Non-Registered Api Provider cannot be updated  

* Pre-Conditions:
  
  Api Provider was not registered previously.

* Actions:

  Update Api Provider onboardingDetails
  
  Request Body: [request body]

* Post-Conditions:
  
  404 Not found.

## Test Case 5: Partially Update Registered Api Provider  
  
  This test case will check that a Registered Api Provider can be partially updated  

* Pre-Conditions:
  
  Api Provider was registered previously and there is a {registerId} for his Api Provider in the DB

* Actions:

  Update Api Provider onboardingDetails
  
  Request Body: [request body]

* Post-Conditions:
  
  200 API invoker details updated successfully.

## Test Case 6: Partially Update Not Registered Api Provider 
  
  This test case will check that a Non-Registered Api Provider cannot be partially updated  

* Pre-Conditions:
  
  Api Provider was not registered previously.

* Actions:

  Update Api Provider onboardingDetails
  
  Request Body: [request body]

* Post-Conditions:
  
  404 Not found.

## Test Case 7: Delete Registered Api Provider   
  
  This test case will check that a Registered Api Provider can be deleted  

* Pre-Conditions:
  
  Api Provider was registered previously.

* Actions:

  Delete Api Provider 


* Post-Conditions:

  204 The individual API Invoker matching registerId was offboarded.

## Test Case 8: Delete Not Registered Api Provider

  This test case will check that a Non-Registered Api Provider cannot be deleted

* Pre-Conditions:

  Api Provider was not registered previously.

* Actions:

  Delete Api Provider


* Post-Conditions:

  404 Not Found.



[request body]: ./provider_details_post_example.json  "API Invoker Request"

[Return To All Test Plans]: ../README.md