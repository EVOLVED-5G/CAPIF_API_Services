- [Test Plan for CAPIF Discover Service](#test-plan-for-capif-discover-service)
- [Tests](#tests)
  - [Test Case 1: Discover Published service APIs by Authorised API Invoker](#test-case-1-discover-published-service-apis-by-authorised-api-invoker)


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


  api_invoker_id, api_name, api_version, comm_type, protocol, aef_id, data_format, api_cat, supported_features, api_supported_features