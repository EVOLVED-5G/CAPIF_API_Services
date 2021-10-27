- [Test Plan for CAPIF Api Provider Management](#test-plan-for-capif-api-provider-management)
- [Tests](#tests)
  - [Test Case 1: Register new API Provider](#test-case-1-register-new-api-provider)
  - [Test Case 2: Register API Provider Already registered](#test-case-2-register-api-provider-already-registered)


# Test Plan for CAPIF Api Provider Management
At this documentation you will have all information and related files and examples of test plan for this API.

# Tests

## Test Case 1: Register new API Provider
  
  This test case will check if a registration of new API provider are OK 

* Pre-Conditions:
  
  NetApp was not registered previously.

* Actions:

  Register provider

  Request Body: TBD

* Post-Conditions:
  
  201 Created, API provider domain registered successfully.




## Test Case 2: Register API Provider Already registered

  This test case will check if a registration of API provider previously registered return the properly response 

* Pre-Conditions:
  
  NetApp was registered previously.

* Actions:

  Register provider
  
  Request Body: TBD

* Post-Conditions:
  
  403 Forbidden returned.