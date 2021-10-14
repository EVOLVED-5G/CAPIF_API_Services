- [Test Plan for CAPIF Api Invoker Management](#test-plan-for-capif-api-invoker-management)
- [Tests](#tests)
  - [Test Case 1: Register NetApp](#test-case-1-register-netapp)
  - [Test Case 2: Register NetApp Already registered](#test-case-2-register-netapp-already-registered)
  - [Test Case 2: Register NetApp Already registered](#test-case-2-register-netapp-already-registered-1)


# Test Plan for CAPIF Api Invoker Management
At this documentation you will have all information and related files and examples of test plan for this API.

# Tests

## Test Case 1: Register NetApp
  
  This test case will check if a registration of new NetApp are OK 

* Pre-Conditions:
  
  NetApp was not registered previously.

* Actions:

  Register NetApp
  
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  201 Created, API invoker on-boarded successfully.

  Header Location at response contains the URI of the newly created resource, according to the structure: {apiRoot}/api-invoker-management/v1/onboardedInvokers/{onboardingId}


## Test Case 2: Register NetApp Already registered
  
  This test case will check if a registration of NetApp previously registered return the properly response 

* Pre-Conditions:
  
  NetApp was registered previously.

* Actions:

  Register NetApp
  
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  403 Forbidden returned.

## Test Case 2: Register NetApp Already registered
  
  Prueba 3

* Pre-Conditions:
  
  NetApp was registered previously.

* Actions:

  Register NetApp
  
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  403 Forbidden returned.