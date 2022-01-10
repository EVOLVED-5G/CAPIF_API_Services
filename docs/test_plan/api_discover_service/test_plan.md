- [Test Plan for CAPIF Discover Service](#test-plan-for-capif-discover-service)
- [Tests](#tests)
  - [Test Case 1: Discover Published service APIs by Authorised API Invoker](#test-case-1-discover-published-service-apis-by-authorised-api-invoker)
  - [Test Case 2: Discover Published service APIs by Non Authorised API Invoker](#test-case-2-discover-published-service-apis-by-non-authorised-api-invoker)
  - [Test Case 3: Discover Published service APIs by not registered API Invoker](#test-case-3-discover-published-service-apis-by-not-registered-api-invoker)
  - [Test Case 4: Discover Published service APIs by registered API Invoker with 1 result filtered](#test-case-4-discover-published-service-apis-by-registered-api-invoker-with-1-result-filtered)
  - [Test Case 5: Discover Published service APIs by registered API Invoker filtered with no match](#test-case-5-discover-published-service-apis-by-registered-api-invoker-filtered-with-no-match)
  - [Test Case 6: Discover Published service APIs by registered API Invoker not filtered](#test-case-6-discover-published-service-apis-by-registered-api-invoker-not-filtered)


# Test Plan for CAPIF Discover Service
At this documentation you will have all information and related files and examples of test plan for this API.

# Tests

## Test Case 1: Discover Published service APIs by Authorised API Invoker
  
  This test case will check that an API Publisher can Publish an API 

* Pre-Conditions: 
  
  API service is previously registered at CAPIF core with api-invoker-id

* Actions:

  GET service

* Post-Conditions:

  Retrieve the collection of APIs assigned to this api invoker
  
  200 With Collection of Service API Descriptions 

## Test Case 2: Discover Published service APIs by Non Authorised API Invoker
  
  This test case will check that an API Publisher can't discover published APIs 

* Pre-Conditions: 
  
  API service is previously registered at CAPIF core with api-invoker-id

* Actions:

  GET service

* Post-Conditions:
  
  401 Unauthorized 

## Test Case 3: Discover Published service APIs by not registered API Invoker
  
  This test case will check that a not registered invoker is forbidden to discover published APIs  

* Pre-Conditions: 
  
  API service is previously registered at CAPIF core with api-invoker-id with 2 API services registered

* Actions:

  GET service filtered by name

* Post-Conditions:
  
  403 Forbidden

## Test Case 4: Discover Published service APIs by registered API Invoker with 1 result filtered
  
  This test case will check that a registered invoker search of one specific API through discover published APIs  

* Pre-Conditions: 
  
  API service is previously registered at CAPIF core with api-invoker-id with 2 API services registered

* Actions:

  GET service with api-name query parameter with one registered name

* Post-Conditions:
  
  200 Ok with 1 api returned

## Test Case 5: Discover Published service APIs by registered API Invoker filtered with no match
  
  This test case will check that a registered invoker search of not present API through discover published APIs  

* Pre-Conditions: 
  
  API service is previously registered at CAPIF core with api-invoker-id with 2 API services registered

* Actions:

  GET service with api-name query parameter with not registered name

* Post-Conditions:
  
  200 Ok with empty list returned

## Test Case 6: Discover Published service APIs by registered API Invoker not filtered
  
  This test case will check that a registered invoker search of not present API through discover published APIs  

* Pre-Conditions: 
  
  API service is previously registered at CAPIF core with api-invoker-id with 2 API services registered

* Actions:

  GET service without api-name query parameter

* Post-Conditions:
  
  200 Ok with 2 api returned
