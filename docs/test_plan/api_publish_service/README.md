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
* **Test ID**: ***capif_api_publish_service-1***
* **Description**:
  
  This test case will check that an API Publisher can Publish an API 
* **Pre-Conditions**:
  
  * CAPIF subscriber is pre-authorised (has valid apfId from CAPIF Authority)

* **Information of Test**:
  1. Perform [Provider Registration]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Use APF Certificate

* **Execution Steps**:
  1. Register Provider at CCF and store certificates.
  2. Publish Service API
  3. Retrieve {apiId} from body and Location header with new resource created from response
   
* **Expected Result**:
  1. Response to Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId}*

  2. Published Service API is stored in CAPIF Database

## Test Case 2: Publish API by NON Authorised API Publisher
* **Test ID**: ***capif_api_publish_service-2***
* **Description**:
  
  This test case will check that an API Publisher cannot Publish an API withot valid apfId 
* **Pre-Conditions**:
  
  * CAPIF subscriber is NOT pre-authorised (has invalid apfId from CAPIF Authority)

* **Information of Test**:
  1. Perform [Provider Registration]

  2. Publish Service API with invalid APF ID at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{APF_ID_NOT_VALID}/service-apis*
     * body [service api description] with apiName service_1
     * Use APF Certificate

* **Execution Steps**:
  1. Register Provider at CCF and store certificates.
  2. Publish Service API with invalid APF ID

* **Expected Result**:
  1. Response to Publish request must accomplish:
     1. **401 Unauthorized**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status **401**
        * title with message "Unauthorized"
        * detail with message "Publisher not existing".
        * cause with message "Publisher id not found".

  2. Service API is NOT stored in CAPIF Database


## Test Case 3: Retrieve all APIs Published by Authorised apfId 
* **Test ID**: ***capif_api_publish_service-3***
* **Description**:

  This test case will check that an API Publisher can Retrieve all API published
* **Pre-Conditions**:

  * CAPIF subscriber is pre-authorised (has valid apfId from CAPIF Authority)
  * At least 2 service APIs are published.

* **Information of Test**:
  1. Perform [Provider Registration]

  2. Publish Service API at CCF:
     * Send Post to *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Get apiId
     * Use APF Certificate

  3. Publish Other Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_2
     * Get apiId
     * Use APF Certificate

  4. Retrieve all published APIs:
     * Send Get to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * Use APF Certificate

* **Execution Steps**:
  1. Register Provider at CCF and store certificates.
  2. Publish Service API service_1
  3. Retrieve {apiId1} from body and Location header with new resource created from response
  4. Publish Service API service_2
  5. Retrieve {apiId2} from body and Location header with new resource created from response
  6. Retrieve All published APIs and check if both are present.

* **Expected Result**:
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
* **Test ID**: ***capif_api_publish_service-4***
* **Description**:

  This test case will check that an API Publisher cannot Retrieve API published when apfId is not authorised 
* **Pre-Conditions**:

  * CAPIF subscriber is NOT pre-authorised (has invalid apfId from CAPIF Authority)

* **Information of Test**:
  1. Perform [Provider Registration]

  2. Retrieve all published APIs:
     * Send Get to *https://{CAPIF_HOSTNAME}/published-apis/v1/{APF_ID_NOT_VALID}/service-apis*
     * Use APF Certificate

* **Execution Steps**:
  1. Register Provider at CCF and store certificates.
  2. Retrieve All published APIs
   
* **Expected Result**:
  1. Response to Publish request must accomplish:
     1. **401 Non Authorized**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status **401**
        * title with message "Unauthorized"
        * detail with message "Provider not existing".
        * cause with message "Provider id not found".

  2. Service API is NOT stored in CAPIF Database

## Test Case 5: Retrieve single APIs Published by Authorised apfId
* **Test ID**: ***capif_api_publish_service-5***
* **Description**:
  
  This test case will check that an API Publisher can Retrieve API published one by one
* **Pre-Conditions**:
  
  * CAPIF subscriber is pre-authorised (has valid apfId from CAPIF Authority)
  * At least 2 service APIs are published.

* **Information of Test**:
  1. Perform [Provider Registration]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Get apiId
     * Use APF Certificate

  3. Publish Other Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_2
     * Get apiId
     * Use APF Certificate

  4. Retrieve service_1 published APIs detail:
     * Send Get to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{apiId1}*
     * Use APF Certificate

  5. Retrieve service_2 published APIs detail:
     * Send Get to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{apiId2}*
     * Use APF Certificate

* **Execution Steps**:
  1. Register Provider at CCF and store certificates.
  2. Publish Service API service_1.
  3. Retrieve {apiId1} from body and Location header with new resource created from response.
  4. Publish Service API service_2.
  5. Retrieve {apiId2} from body and Location header with new resource created from response.
  6. Retrieve service_1 API Detail.
  7. Retrieve service_2 API Detail.

* **Expected Result**:
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
* **Test ID**: ***capif_api_publish_service-6***
* **Description**:
  
  This test case will check that an API Publisher try to get detail of not published api.
* **Pre-Conditions**:
  
  * CAPIF subscriber is pre-authorised (has valid apfId from CAPIF Authority)
  * No published api

* **Information of Test**:
  1. Perform [Provider Registration]
  2. Retrieve not published APIs detail:
     * Send Get to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{SERVICE_API_ID_NOT_VALID}*
     * Use APF Certificate

* **Execution Steps**:
  1. Register Provider at CCF and store certificates.
  2. Retrieve not published API Detail.

* **Expected Result**:
  1. Response to Retrieve for NOT published API must accomplish:
     1. **404 Not Found**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status **404**
        * title with message "Not Found"
        * detail with message "Service API not found".
        * cause with message "No Service with specific credentials exists".


## Test Case 7: Retrieve single APIs Published by NON Authorised apfId 
* **Test ID**: ***capif_api_publish_service-7***
* **Description**:
  
  This test case will check that an API Publisher cannot Retrieve detailed API published when apfId is not authorised 
* **Pre-Conditions**:
  
  * CAPIF subscriber is NOT pre-authorised (has invalid apfId from CAPIF Authority)

* **Information of Test**:
  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Get apiId
     * Use APF Certificate

  3. Retrieve detailed published APIs:
     * Send Get to *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/${apiId}*
     * Use Invoker certificate

* **Execution Steps**:
  1. Register Provider at CCF and store certificates.
  2. Publish Service API at CCF
  3. Retrieve {apiId} from body and Location header with new resource created from response.
  4. Register and onboard Invoker at CCF
  5. Store signed Invoker Certificate
  6. Retrieve detailed published API acting as Invoker
   
* **Expected Result**:
  1. Response to Retrieve Detailed published API acting as Invoker must accomplish:
     1. **401 Unauthorized**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status **401**
        * title with message "Unauthorized"
        * detail with message "User not authorized".
        * cause with message "Certificate not authorized".

  2. Service API is NOT stored in CAPIF Database


## Test Case 8: Update API Published by Authorised apfId with valid serviceApiId
* **Test ID**: ***capif_api_publish_service-8***
* **Description**:
  
  This test case will check that an API Publisher can Update published API with a valid serviceApiId 
* **Pre-Conditions**:
  
  * CAPIF subscriber is pre-authorised (has valid apfId from CAPIF Authority)
  * A service APIs is published.

* **Information of Test**:
  1. Perform [Provider Registration]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Get apiId
     * get resource url from location Header.
     * Use APF Certificate

  3. Update published API at CCF:
     * Send PUT to resource URL *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{serivceApiId}*
     * body [service api description] with overrided apiName to service_1_modified
     * Use APF Certificate

  4. Retrieve detail of service API:
     * Send Get to resource URL *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{serivceApiId}*
     * check apiName is service_1_modified
     * Use APF Certificate

* **Execution Steps**:
  1. Register Provider at CCF and store certificates.
  2. Publish Service API
  3. Retrieve {apiId} from body and Location header with new resource url created from response
  4. Update published Service API.
  5. Retrieve detail of Service API
   
* **Expected Result**:
  1. Response to Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId}*

  2. Response to Update Published Service API:
     1. **200 OK**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiName service_1_modified

  3. Response to Retrieve detail of Service API:
     1. **200 OK**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiName service_1_modified.
  

## Test Case 9: Update APIs Published by Authorised apfId with invalid serviceApiId  
* **Test ID**: ***capif_api_publish_service-9***
* **Description**:
  
  This test case will check that an API Publisher cannot Update published API with a invalid serviceApiId
* **Pre-Conditions**:
  
  * CAPIF subscriber is pre-authorised (has valid apfId from CAPIF Authority)

* **Information of Test**:
  1. Perform [Provider Registration]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Get apiId
     * Use APF Certificate

  3. Update published API at CCF:
     * Send PUT to resource URL *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{SERVICE_API_ID_NOT_VALID}*
     * body [service api description] with overrided apiName to ***service_1_modified***
     * Use APF Certificate

* **Execution Steps**:
  1. Register Provider at CCF and store certificates.
  2. Update published Service API.
   
* **Expected Result**:
  1. Response to Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId}*

  2. Response to Update Published Service API:
     1. **404 Not Found**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status **404**
        * title with message "Not Found"
        * detail with message "Service API not found".
        * cause with message "Service API id not found".

  ## Test Case 10: Update APIs Published by NON Authorised apfId  
* **Test ID**: ***capif_api_publish_service-10***
* **Description**:
  
  This test case will check that an API Publisher cannot Update API published when apfId is not authorised
* **Pre-Conditions**:
  
  * CAPIF subscriber is NOT pre-authorised (has invalid apfId from CAPIF Authority)

* **Information of Test**:
  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Get apiId
     * Use APF Certificate

  3. Update published API at CCF:
     * Send PUT to resource URL *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{serviceApiId}*
     * body [service api description] with overrided apiName to ***service_1_modified***
     * Use invoker certificate

  4.  Retrieve detail of service API:
     * Send Get to resource URL *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{serivceApiId}*
     * check apiName is service_1
     * Use APF Certificate

* **Execution Steps**:
  1. Register Provider at CCF and store certificates.
  2. Publish Service API at CCF
  3. Retrieve {apiId} from body and Location header with new resource created from response.
  4. Register and onboard Invoker at CCF
  5. Store signed Invoker Certificate
  6. Update published API at CCF as Invoker
  7. Retrieve detail of Service API as publisher
   
* **Expected Result**:
  1. Response to Update published API acting as Invoker must accomplish:
     1. **401 Unauthorized**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status **401**
        * title with message "Unauthorized"
        * detail with message "User not authorized".
        * cause with message "Certificate not authorized".

  2. Response to Retrieve Detail of Service API:
     1. **200 OK**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiName service_1.


## Test Case 11: Delete API Published by Authorised apfId with valid serviceApiId
* **Test ID**: ***capif_api_publish_service-11***
* **Description**:
  
  This test case will check that an API Publisher can Delete published API with a valid serviceApiId
* **Pre-Conditions**:
  
  * CAPIF subscriber is pre-authorised (has valid apfId from CAPIF Authority).
  * A service APIs is published.

* **Information of Test**:
  1. Perform [Provider Registration]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Get apiId
     * Use APF Certificate

  3. Remove published Service API at CCF:
     * Send DELETE to resource URL *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{serviceApiId}*
     * Use APF Certificate
  4. Retrieve detail of service API:
     * Send Get to resource URL *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{serivceApiId}*
     * Use APF Certificate

* **Execution Steps**:
  1. Register Provider at CCF and store certificates.
  2. Publish Service API
  3. Retrieve {apiId} from body and Location header with new resource created from response
  4. Remove published API at CCF
  5. Try to retreive deleted service API from CCF
   
* **Expected Result**:
  1. Response to Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId}*

  2. Published Service API is stored in CAPIF Database

  3. Response to Remove published Service API at CCF:
     1. **204 No Content**

  4. Response to Retrieve for DELETED published API must accomplish:
     1. **404 Not Found**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 404
        * title with message "Not Found"
        * detail with message "Service API not found".
        * cause with message "No Service with specific credentials exists".


## Test Case 12: Delete APIs Published by Authorised apfId with invalid serviceApiId
* **Test ID**: ***capif_api_publish_service-12***
* **Description**:
  
  This test case will check that an API Publisher cannot Delete with invalid serviceApiId
* **Pre-Conditions**:
  
  * CAPIF subscriber is pre-authorised (has valid apfId from CAPIF Authority).

* **Information of Test**:
  1. Perform [Provider Registration]

  2. Remove published Service API at CCF with invalid serviceId:
     * Send DELETE to resource URL *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{SERVICE_API_ID_NOT_VALID}*
     * Use APF Certificate

* **Execution Steps**:
  1. Register Provider at CCF and store certificates.
  2. Remove published API at CCF with invalid serviceId
   
* **Expected Result**:
  1. Response to Remove published Service API at CCF:
     1. **404 Not Found**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 404
        * title with message "Not Found"
        * detail with message "Service API not found".
        * cause with message "Service API id not found".


## Test Case 13: Delete APIs Published by NON Authorised apfId
* **Test ID**: ***capif_api_publish_service-12***
* **Description**:
  
  This test case will check that an API Publisher cannot Delete API published when apfId is not authorised
* **Pre-Conditions**:
  
  * CAPIF subscriber is pre-authorised (has valid apfId from CAPIF Authority).

* **Information of Test**:
  1. Perform [Provider Registration] and [Invoker Onboarding]

  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Get apiId
     * Use APF Certificate

  3. Remove published Service API at CCF with invalid serviceId as Invoker:
     * Send DELETE to resource URL *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis/{SERVICE_API_ID_NOT_VALID}*
     * Use invoker certificate.

* **Execution Steps**:
  1. Register Provider at CCF and store certificates.
  2. Register Invoker and onboard Invoker at CCF
  3. Remove published API at CCF with invalid serviceId as Invoker
   
* **Expected Result**:
  1. Response to Remove published Service API at CCF:
     1. **401 Unauthorized**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status **401**
        * title with message "Unauthorized"
        * detail with message "User not authorized".
        * cause with message "Certificate not authorized".


   [service api description]: ./service_api_description_post_example.json  "Service API Description Request"
   [publisher register body]: ./publisher_register_body.json  "Publish register Body"
   [invoker onboarding body]: ../api_invoker_management/invoker_details_post_example.json  "API Invoker Request"
   [invoker register body]: ../api_invoker_management/invoker_register_body.json  "Invoker Register Body"
   [provider request body]: ../api_provider_management/provider_details_post_example.json  "API Provider Enrolment Request"
   [provider request patch body]: ../api_provider_management/provider_details_enrolment_details_patch_example.json  "API Provider Enrolment Patch Request"
   [provider getauth body]: ../api_provider_management/provider_getauth_example.json    "Get Auth Example"

   [invoker onboarding]: ../common_operations/README.md#register-an-invoker "Invoker Onboarding"
   [provider registration]: ../common_operations/README.md#register-a-provider "Provider Registration"


  [Return To All Test Plans]: ../README.md