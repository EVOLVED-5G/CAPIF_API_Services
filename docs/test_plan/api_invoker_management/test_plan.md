- [Test Plan for CAPIF Api Invoker Management](#test-plan-for-capif-api-invoker-management)
- [Tests](#tests)
  - [Test Case 1: Register NetApp](#test-case-1-register-netapp)
  - [Test Case 2: Register NetApp Already registered](#test-case-2-register-netapp-already-registered)
  - [Test Case 3: Update Registered NetApp](#test-case-3-update-registered-netapp)
  - [Test Case 4: Update Not Registered NetApp](#test-case-4-update-not-registered-netapp)
  - [Test Case 5: Delete Registered NetApp](#test-case-5-delete-registered-netapp)
  - [Test Case 6: Delete Not Registered NetApp](#test-case-6-delete-not-registered-netapp)


# Test Plan for CAPIF Api Invoker Management
At this documentation you will have all information and related files and examples of test plan for this API.

# Tests

## Test Case 1: Register NetApp
  
  This test case will check that NetApp can be registered 

* Pre-Conditions:
  
  NetApp was not registered previously.

* Actions:

  Register NetApp
  
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  201 API invoker on-boarded successfully.

  Header Location at response contains the URI of the newly created resource, according to the structure: {apiRoot}/api-invoker-management/v1/onboardedInvokers/{onboardingId}


## Test Case 2: Register NetApp Already registered
  
  This test case will check that a NetApp previously registered canot be re-registered

* Pre-Conditions:
  
  NetApp was registered previously and there is a {onboardingId} for his NetApp in the DB

* Actions:

  Register NetApp
  
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  403 Forbidden returned.

## Test Case 3: Update Registered NetApp  
  
  This test case will check that a Registered NetApp can be updated  

* Pre-Conditions:
  
  NetApp was registered previously and there is a {onboardingId} for his NetApp in the DB

* Actions:

  Update NetApp onboardingDetails
  
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  200 API invoker details updated successfully.

## Test Case 4: Update Not Registered NetApp 
  
  This test case will check that a Non-Registered NetApp cannot be updated  

* Pre-Conditions:
  
  NetApp was not registered previously.

* Actions:

  Update NetApp onboardingDetails
  
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  404 Not found.

## Test Case 5: Delete Registered NetApp   
  
  This test case will check that a Registered NetApp can be deleted  

* Pre-Conditions:
  
  NetApp was registered previously.

* Actions:

  Delete NetApp 
  
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  204 The individual API Invoker matching onboardingId was offboarded.

## Test Case 6: Delete Not Registered NetApp 
  
  This test case will check that a Non-Registered NetApp cannot be deleted  

* Pre-Conditions:
  
  NetApp was not registered previously.

* Actions:

  Delete NetApp 
  
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  404 Not Found.
