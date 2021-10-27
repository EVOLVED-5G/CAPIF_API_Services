- [Test Plan for CAPIF Api Publish Service](#test-plan-for-capif-api-publish-service)
- [Tests](#tests)
  - [Test Case 1: Publish API by Authorised API Publisher](#test-case-1-publish-api-by-authorised-api-publisher)
  - [Test Case 2: Publish API by NON Authorised API Publisher](#test-case-2-publish-api-by-non-authorised-api-publisher)
  - [Test Case 3: Retrieve all APIs Published by Authorised apfId](#test-case-3-retrieve-all-apis-published-by-authorised-apfid)
  - [Test Case 4: Retrieve all APIs Published by NON Authorised apfId](#test-case-4-retrieve-all-apis-published-by-non-authorised-apfid)
  - [Test Case 5: Retrieve single APIs Published by Authorised apfId](#test-case-5-retrieve-single-apis-published-by-authorised-apfid)
  - [Test Case 6: Retrieve single APIs non Published by Authorised apfId](#test-case-6-retrieve-single-apis-non-published-by-authorised-apfid)
  - [Test Case 7: Retrieve single APIs Published by NON Authorised apfId](#test-case-7-retrieve-single-apis-published-by-non-authorised-apfid)
  - [Test Case 8: Update API Published by Authorised apfId with valid serviceApiId](#test-case-8-update-api-published-by-authorised-apfid-with-valid-serviceapiid)
  - [Test Case 9: Update APIs Published by Authorised apfId with invalid serviceApiId](#test-case-9-update-apis-published-by-authorised-apfid-with-invalid-serviceapiid)
  - [Test Case 10: Update APIs Published by NON Authorised apfId](#test-case-10-update-apis-published-by-non-authorised-apfid)
  - [Test Case 11: Delete API Published by Authorised apfId with valid serviceApiId](#test-case-11-delete-api-published-by-authorised-apfid-with-valid-serviceapiid)
  - [Test Case 12: Delete APIs Published by Authorised apfId with invalid serviceApiId](#test-case-12-delete-apis-published-by-authorised-apfid-with-invalid-serviceapiid)
  - [Test Case 13: Delete APIs Published by NON Authorised apfId](#test-case-13-delete-apis-published-by-non-authorised-apfid)


# Test Plan for CAPIF Api Publish Service
At this documentation you will have all information and related files and examples of test plan for this API.

# Tests

## Test Case 1: Publish API by Authorised API Publisher
  
  This test case will check that an API Publisher can Publish an API 

* Pre-Conditions: 
  
  API Publisher is pre-authorised to publish APIs by getting a valid apfId from CAPIF Authority 

* Actions:

  POST Publish API
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  API details are stored in CAPIF Database

  201 API Published 

  Service API published successfully The URI of the created resource shall be returned in the "Location" HTTP header. 

  Location Contains the URI of the newly created resource, according to the structure: {apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId}

## Test Case 2: Publish API by NON Authorised API Publisher
  
  This test case will check that an API Publisher cannot Publish an API withot valid apfId

* Pre-Conditions:  
  
  API Publisher is NOT pre-authorised to publish APIs and has invalid apfId

* Actions:

  POST Publish API
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  API is not included in the Database

  401 Unauthorised
  
## Test Case 3: Retrieve all APIs Published by Authorised apfId 
  
  This test case will check that an API Publisher can Retrieve all API published 

* Pre-Conditions: 
  
  API Publisher is pre-authorised to publish APIs by getting a valid apfId from CAPIF Authority 

* Actions:

  GET Retrieve APIs
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  200 Definition of all service API(s) published by the API publishing function.

## Test Case 4: Retrieve all APIs Published by NON Authorised apfId 
  
  This test case will check that an API Publisher cannot Retrieve API published when apfId is not authorised 

* Pre-Conditions: 
  
  API Publisher with apgId is not authorised to publish APIs

* Actions:

  GET Retrieve APIs
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  401 Unauthorized

## Test Case 5: Retrieve single APIs Published by Authorised apfId 
  
  This test case will check that an API Publisher can Retrieve an API published details

* Pre-Conditions: 
  
  API Publisher is pre-authorised to publish APIs by getting a valid apfId from CAPIF Authority 

  API has been published an has valid serviceApiId
  
* Actions:

  GET Retrieve API details for serviceApiId
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  200 Definition of serviceApiId service API published by the API publishing function.

## Test Case 6: Retrieve single APIs non Published by Authorised apfId 
  
  This test case will check that an API Publisher cannot Retrieve API published when apfId is not authorised 

* Pre-Conditions: 
  
  API Publisher is pre-authorised to publish APIs by getting a valid apfId from CAPIF Authority 

  API has not been published an has in valid serviceApiId

* Actions:

  GET Retrieve API details for serviceApiId
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  404 Not Found

## Test Case 7: Retrieve single APIs Published by NON Authorised apfId 
  
  This test case will check that an API Publisher cannot Retrieve API details of non published APIs 

* Pre-Conditions: 
  
  API Publisher is non-authorised to publish APIs and has an invalid apfId 

* Actions:

  GET Retrieve API details for serviceApiId
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  401 Unauthorized

## Test Case 8: Update API Published by Authorised apfId with valid serviceApiId 
  
  This test case will check that an API Publisher can Update published API with a valid serviceApiId

* Pre-Conditions: 
  
  API Publisher is pre-authorised to publish APIs by getting a valid apfId from CAPIF Authority 

  API has been published an has valid serviceApiId

* Actions:

  PUT Update APIs
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  200 Definition of service API updated successfully.

## Test Case 9: Update APIs Published by Authorised apfId with invalid serviceApiId  
  
  This test case will check that an API Publisher cannot Update API published when API has not been published 

* Pre-Conditions: 

  API Publisher is pre-authorised to publish APIs by getting a valid apfId from CAPIF Authority 

  API has not been published an has invalid serviceApiId
* Actions:

  PUT Update APIs
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  404 Not Found

  ## Test Case 10: Update APIs Published by NON Authorised apfId  
  
  This test case will check that an API Publisher cannot Update API published when apfId is not authorised 

* Pre-Conditions: 
  
  API Publisher is non-authorised to publish APIs and has invalid apfId  

* Actions:

  PUT Update APIs
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  401 Unauthorized

## Test Case 11: Delete API Published by Authorised apfId with valid serviceApiId
  
  This test case will check that an API Publisher can Delete published API with a valid serviceApiId

* Pre-Conditions: 
  
  API Publisher is pre-authorised to publish APIs by getting a valid apfId from CAPIF Authority 

  API has been published an has valid serviceApiId

* Actions:

  DELETE API
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  204 The individual published service API matching the serviceAPiId is deleted.

## Test Case 12: Delete APIs Published by Authorised apfId with invalid serviceApiId
  
  This test case will check that an API Publisher cannot Delete API published when API has not been published 

* Pre-Conditions: 

  API Publisher is pre-authorised to publish APIs by getting a valid apfId from CAPIF Authority 

  API has not been published an has invalid serviceApiId
* Actions:

  DELETE API
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  404 Not Found

## Test Case 13: Delete APIs Published by NON Authorised apfId 
  
  This test case will check that an API Publisher cannot Delete API published when apfId is not authorised 

* Pre-Conditions: 
  
  API Publisher is non-authorised to publish APIs and has invalid apfId  

* Actions:

  DELETE API
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  401 Unauthorized