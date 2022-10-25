[**[Return To All Test Plans]**]

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
* Test ID: ***capif_api_publish_service-1***
* Description:
  
  This test case will check that an API Publisher can Publish an API 
* Pre-Conditions:
  
  * CAPIF subscriber is pre-authorised (has valid apfId from CAPIF Authority)

* Information of Test:

  1. Create public and private key at publisher

  2. Register of Publisher at CCF:
     * Send POST to http://{CAPIF_HOSTNAME}:{CAPIF_HTTP_PORT}/register 
     * body [publisher register body]
     * Get subscriberId
     * Get ccf_publish_url

 3. Publish Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_1
     * Get apiId

* Execution Steps:
  
  1. Register Publisher at CCF
  2. Store signed Certificate
  3. Publish Service API
  4. Retrieve {apiId} from body and Location header with new resource created from response
   
* Expected Result:

  1. Response to Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId}*

  3. Published Service API is stored in CAPIF Database

## Test Case 2: Publish API by NON Authorised API Publisher
* Test ID: ***capif_api_publish_service-2***
* Description:
  
  This test case will check that an API Publisher cannot Publish an API withot valid apfId 
* Pre-Conditions:
  
  * CAPIF subscriber is NOT pre-authorised (has invalid apfId from CAPIF Authority)

* Information of Test:

  1. Create public and private key at publisher

  2. Register of Publisher at CCF:
     * Send POST to http://{CAPIF_HOSTNAME}:{CAPIF_HTTP_PORT}/register 
     * body [publisher register body]
     * Get subscriberId
     * Get ccf_publish_url

 3. Publish Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{APF_ID_NOT_VALID}/service-apis
     * body [service api description] with apiName service_1

* Execution Steps:
  
  1. Register Publisher at CCF
  2. Store signed Certificate
  3. Publish Service API
   
* Expected Result:

  1. Response to Publish request must accomplish:
     1. **401 Non Authorized**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * detail with message "Exposer not existing".
        * cause with message "Exposer id not found".
        * status 401
        * title with message "Unauthorized"

  2. Service API is NOT stored in CAPIF Database


## Test Case 3: Retrieve all APIs Published by Authorised apfId 
* Test ID: ***capif_api_publish_service-3***
* Description:
  
  This test case will check that an API Publisher can Retrieve all API published
* Pre-Conditions:
  
  * CAPIF subscriber is pre-authorised (has valid apfId from CAPIF Authority)

* Information of Test:

  1. Create public and private key at publisher

  2. Register of Publisher at CCF:
     * Send POST to http://{CAPIF_HOSTNAME}:{CAPIF_HTTP_PORT}/register 
     * body [publisher register body]
     * Get subscriberId
     * Get ccf_publish_url

 1. Publish Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_1
     * Get apiId
  
 2. Publish Other Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_2
     * Get apiId

 3. Retrieve all published APIs:
     * Send Get to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis

* Execution Steps:
  
  1. Register Publisher at CCF
  2. Store signed Certificate
  3. Publish Service API service_1
  4. Retrieve {apiId1} from body and Location header with new resource created from response
  5. Publish Service API service_2
  6. Retrieve {apiId2} from body and Location header with new resource created from response
  7. Retrieve All published APIs and check if both are present.


* Expected Result:

  1. Response to service 1 Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId1}*
  2. Response to service 2 Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId2}*
  3. Published Service APIs are stored in CAPIF Database 
  4. Response to Retrieve all published APIs:
     1. **200 OK**
     2. Response body must return an array of **ServiceAPIDescription** data.
     3. Array must contain all previously published APIs.

## Test Case 4: Retrieve all APIs Published by NON Authorised apfId 
* Test ID: ***capif_api_publish_service-4***
* Description:
  
  This test case will check that an API Publisher cannot Retrieve API published when apfId is not authorised 
* Pre-Conditions:
  
  * CAPIF subscriber is NOT pre-authorised (has invalid apfId from CAPIF Authority)

* Information of Test:

  1. Create public and private key at publisher

  2. Register of Publisher at CCF:
     * Send POST to http://{CAPIF_HOSTNAME}:{CAPIF_HTTP_PORT}/register 
     * body [publisher register body]
     * Get subscriberId
     * Get ccf_publish_url

 3. Retrieve all published APIs:
     * Send Get to https://{CAPIF_HOSTNAME}/published-apis/v1/{APF_ID_NOT_VALID}/service-apis

* Execution Steps:
  
  1. Register Publisher at CCF
  2. Store signed Certificate
  3. Retrieve All published APIs
   
* Expected Result:

  1. Response to Publish request must accomplish:
     1. **401 Non Authorized**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * detail with message "Exposer not existing".
        * cause with message "Exposer id not found".
        * status 401
        * title with message "Unauthorized"

  2. Service API is NOT stored in CAPIF Database

## Test Case 5: Retrieve single APIs Published by Authorised apfId
* Test ID: ***capif_api_publish_service-5***
* Description:
  
  This test case will check that an API Publisher can Retrieve API published one by one
* Pre-Conditions:
  
  * CAPIF subscriber is pre-authorised (has valid apfId from CAPIF Authority)

* Information of Test:

  1. Create public and private key at publisher

  2. Register of Publisher at CCF:
     * Send POST to http://{CAPIF_HOSTNAME}:{CAPIF_HTTP_PORT}/register 
     * body [publisher register body]
     * Get subscriberId
     * Get ccf_publish_url

 1. Publish Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_1
     * Get apiId
  
 2. Publish Other Service API at CCF:
     * Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
     * body [service api description] with apiName service_2
     * Get apiId

 3. Retrieve service_1 published APIs detail:
     * Send Get to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{apiId1}

 4. Retrieve service_2 published APIs detail:
     * Send Get to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{apiId2}

* Execution Steps:
  
  1. Register Publisher at CCF
  2. Store signed Certificate
  3. Publish Service API service_1
  4. Retrieve {apiId1} from body and Location header with new resource created from response
  5. Publish Service API service_2
  6. Retrieve {apiId2} from body and Location header with new resource created from response
  7. Retrieve service_1 API Detail.
  8. Retrieve service_2 API Detail.


* Expected Result:

  1. Response to service 1 Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId1}*
  2. Response to service 2 Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId2}*

  3. Published Service APIs are stored in CAPIF Database 
  4. Response to Retrieve service_1 published API using apiId1:
     1. **200 OK**
     2. Response body must return a **ServiceAPIDescription** data.
     3. Array must contain same information than service_1 published registration response.
  5. Response to Retrieve service_2 published API using apiId2:
     1. **200 OK**
     2. Response body must return a **ServiceAPIDescription** data.
     3. Array must contain same information than service_2 published registration response.


## Test Case 6: Retrieve single APIs non Published by Authorised apfId 
  
  This test case will check that an API Publisher cannot Retrieve API published when apfId is not authorised 

* Pre-Conditions: 
  
  API Publisher is pre-authorised to publish APIs by getting a valid apfId from CAPIF Authority 

  API has not been published an has in valid serviceApiId

* Actions:

  GET Retrieve API details for serviceApiId
    
  Request Body: [request body]

* Post-Conditions:
  
  404 Not Found

## Test Case 7: Retrieve single APIs Published by NON Authorised apfId 
  
  This test case will check that an API Publisher cannot Retrieve API details of non published APIs 

* Pre-Conditions: 
  
  API Publisher is non-authorised to publish APIs and has an invalid apfId 

* Actions:

  GET Retrieve API details for serviceApiId
    
  Request Body: [request body]

* Post-Conditions:
  
  401 Unauthorized

## Test Case 8: Update API Published by Authorised apfId with valid serviceApiId 
  
  This test case will check that an API Publisher can Update published API with a valid serviceApiId

* Pre-Conditions: 
  
  API Publisher is pre-authorised to publish APIs by getting a valid apfId from CAPIF Authority 

  API has been published an has valid serviceApiId

* Actions:

  PUT Update APIs
    
  Request Body: [request body]

* Post-Conditions:
  
  200 Definition of service API updated successfully.

## Test Case 9: Update APIs Published by Authorised apfId with invalid serviceApiId  
  
  This test case will check that an API Publisher cannot Update API published when API has not been published 

* Pre-Conditions: 

  API Publisher is pre-authorised to publish APIs by getting a valid apfId from CAPIF Authority 

  API has not been published an has invalid serviceApiId
* Actions:

  PUT Update APIs
    
  Request Body: [request body]

* Post-Conditions:
  
  404 Not Found

  ## Test Case 10: Update APIs Published by NON Authorised apfId  
  
  This test case will check that an API Publisher cannot Update API published when apfId is not authorised 

* Pre-Conditions: 
  
  API Publisher is non-authorised to publish APIs and has invalid apfId  

* Actions:

  PUT Update APIs
    
  Request Body: [request body]

* Post-Conditions:
  
  401 Unauthorized

## Test Case 11: Delete API Published by Authorised apfId with valid serviceApiId
  
  This test case will check that an API Publisher can Delete published API with a valid serviceApiId

* Pre-Conditions: 
  
  API Publisher is pre-authorised to publish APIs by getting a valid apfId from CAPIF Authority 

  API has been published an has valid serviceApiId

* Actions:

  DELETE API
    
  Request Body: [request body]

* Post-Conditions:
  
  204 The individual published service API matching the serviceAPiId is deleted.

## Test Case 12: Delete APIs Published by Authorised apfId with invalid serviceApiId
  
  This test case will check that an API Publisher cannot Delete API published when API has not been published 

* Pre-Conditions: 

  API Publisher is pre-authorised to publish APIs by getting a valid apfId from CAPIF Authority 

  API has not been published an has invalid serviceApiId
* Actions:

  DELETE API
    
  Request Body: [request body]

* Post-Conditions:
  
  404 Not Found

## Test Case 13: Delete APIs Published by NON Authorised apfId 
  
  This test case will check that an API Publisher cannot Delete API published when apfId is not authorised 

* Pre-Conditions: 
  
  API Publisher is non-authorised to publish APIs and has invalid apfId  

* Actions:

  DELETE API
    
  Request Body: [request body]

* Post-Conditions:
  
  401 Unauthorized


  [service api description]: ./service_api_description_post_example.json  "Service API Description Request"
  [publisher register body]: ./publisher_register_body.json


  [Return To All Test Plans]: ../README.md