[**[Return To All Test Plans]**]

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
* **Test ID**: ***capif_api_discover_service-1***
* **Description**:

  This test case will check if NetApp (Invoker) can discover published service APIs.
* **Pre-Conditions**:
  * Service APIs are published.
  * NetApp was registered previously
  * NetApp was onboarded previously with {onboardingId}
  
* **Information of Test**:
  1. Perform [Provider Registration] and [Invoker Onboarding]
  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Use APF Certificate
  3. Request Discover Published APIs:
     * Send GET to *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}*
     * Param api-invoker-id is mandatory
     * Use Invoker Certificate

* **Execution Steps**:
  
  1. Register Provider at CCF, store certificates and Publish Service API at CCF
  2. Register Invoker and Onboard Invoker at CCF
  3. Discover Service APIs by Invoker

* **Expected Result**:

  1. Response to Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId}*

  2. Response to Onboard request must accomplish:
     1. **201 Created**
     2. Response Body must follow **APIInvokerEnrolmentDetails** data structure with:
        * apiInvokerId
        * onboardingInformation->apiInvokerCertificate must contain the public key signed.
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/api-invoker-management/{apiVersion}/onboardedInvokers/{onboardingId}*
  3. Response to Discover Request By Invoker:
     1. **200 OK** response.
     2. Response body must follow **DiscoveredAPIs** data structure:
        * Check if DiscoveredAPIs contains the API Published previously


## Test Case 2: Discover Published service APIs by Non Authorised API Invoker
* **Test ID**: ***capif_api_discover_service-2***
* **Description**:

  This test case will check that an API Publisher can't discover published APIs because is not authorized.

* **Pre-Conditions**:
  * Service APIs are published.
  
* **Information of Test**:
  1. Perform [Provider Registration] and [Invoker Onboarding]
  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Use APF Certificate
  3.  Request Discover Published APIs by no invoker entity:
     * Send GET to *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}*
     * Param api-invoker-id is mandatory
     * Use not Invoker Certificate

* **Execution Steps**:
  1. Register Provider at CCF, store certificates and Publish Service API at CCF
  2. Register Invoker and Onboard Invoker at CCF
  3. Discover Service APIs by no invoker entity

* **Expected Result**:

  1. Response to Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId}*

  2. Response to Onboard request must accomplish:
     1. **201 Created**
     2. Response Body must follow **APIInvokerEnrolmentDetails** data structure with:
        * apiInvokerId
        * onboardingInformation->apiInvokerCertificate must contain the public key signed.
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/api-invoker-management/{apiVersion}/onboardedInvokers/{onboardingId}*

  3. Response to Discover Request By no invoker entity:
     1. **401 Unauthorized**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 401
        * title with message "Unauthorized"
        * detail with message "User not authorized".
        * cause with message "Certificate not authorized".


## Test Case 3: Discover Published service APIs by not registered API Invoker
* **Test ID**: ***capif_api_discover_service-3***
* **Description**:

  This test case will check that a not registered invoker is forbidden to discover published APIs.

* **Pre-Conditions**:
  * Service APIs are published.
  
* **Information of Test**:
  1. Perform [Provider Registration] and [Invoker Onboarding]
  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Use APF Certificate
  3.  Request Discover Published APIs with not valid apiInvoker:
     * Send GET to *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={INVOKER_NOT_REGISTERED}*
     * Param api-invoker-id is mandatory
     * Using invoker certificate

* **Execution Steps**:
  1. Register Provider at CCF, store certificates and Publish Service API at CCF
  2. Register Invoker and Onboard Invoker at CCF
  3. Discover Service APIs by Publisher

* **Expected Result**:
  1. Response to Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId}*

  2. Response to Onboard request must accomplish:
     1. **201 Created**
     2. Response Body must follow **APIInvokerEnrolmentDetails** data structure with:
        * apiInvokerId
        * onboardingInformation->apiInvokerCertificate must contain the public key signed.
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/api-invoker-management/{apiVersion}/onboardedInvokers/{onboardingId}*

  3. Response to Discover Request By Invoker:
     1. **404 Not Found**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 404
        * title with message "Not Found"
        * detail with message "API Invoker does not exist".
        * cause with message "API Invoker id not found".


## Test Case 4: Discover Published service APIs by registered API Invoker with 1 result filtered
* **Test ID**: ***capif_api_discover_service-4***
* **Description**:

  This test case will check if NetApp (Invoker) can discover published service APIs.
* **Pre-Conditions**:
  * At least 2 Service APIs are published.
  * NetApp was registered previously
  * NetApp was onboarded previously with {onboardingId}
  
* **Information of Test**:
  1. Perform [Provider Registration] and [Invoker Onboarding]
  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Use APF Certificate
  3. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_2
     * Use APF Certificate
  4.  Request Discover Published APIs filtering by api-name:
     * Send GET to ccf_discover_url *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}&api-name=service_1*
     * Param api-invoker-id is mandatory
     * Using invoker certificate
     * filter by api-name service_1

* **Execution Steps**:
  1. Register Provider at CCF, store certificates and Publish Service API service_1 and service_2 at CCF
  2. Register Invoker and Onboard Invoker at CCF
  3. Discover Service APIs by Invoker.
  4. Discover filtered by api-name service_1 Service APIs by Invoker

* **Expected Result**:
  1. Response to Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId}*
  2. Response to Onboard request must accomplish:
     1. **201 Created**
     2. Response Body must follow **APIInvokerEnrolmentDetails** data structure with:
        * apiInvokerId
        * onboardingInformation->apiInvokerCertificate must contain the public key signed.
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/api-invoker-management/{apiVersion}/onboardedInvokers/{onboardingId}*
  3. Response to Discover Request By Invoker:
     1. **200 OK** response.
     2. Response body must follow **DiscoveredAPIs** data structure:
        * Check if DiscoveredAPIs contains previously registered Service APIs published.
  4. Response to Discover Request By Invoker:
     1. **200 OK** response.
     2. Response body must follow **DiscoveredAPIs** data structure:
        * Check if DiscoveredAPIs contains only Service API published with api-name service_1


## Test Case 5: Discover Published service APIs by registered API Invoker filtered with no match
* **Test ID**: ***capif_api_discover_service-5***
* **Description**:
  This test case will check if NetApp (Invoker) can discover published service APIs.
* **Pre-Conditions**:
  * At least 2 Service APIs are published.
  * NetApp was registered previously
  * NetApp was onboarded previously with {onboardingId}
  
* **Information of Test**:
  1. Perform [Provider Registration] and [Invoker Onboarding]
  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Use APF Certificate
  3. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_2
     * Use APF Certificate
  4.  Request Discover Published APIs filtering by api-name not published:
     * Send GET to ccf_discover_url *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}&api-name=NOT_VALID_NAME*
     * Param api-invoker-id is mandatory
     * Using invoker certificate
     * filter by api-name NOT_VALID_NAME

* **Execution Steps**:
  1. Register Provider at CCF, store certificates and Publish Service API service_1 and service_2 at CCF
  2. Register Invoker and Onboard Invoker at CCF
  3. Discover Service APIs by Invoker.
  4. Discover filtered by api-name not published Service APIs by Invoker

* **Expected Result**:
  1. Response to Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId}*
  2. Response to Onboard request must accomplish:
     1. **201 Created**
     2. Response Body must follow **APIInvokerEnrolmentDetails** data structure with:
        * apiInvokerId
        * onboardingInformation->apiInvokerCertificate must contain the public key signed.
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/api-invoker-management/{apiVersion}/onboardedInvokers/{onboardingId}*
  3. Response to Discover Request By Invoker:
     1. **200 OK** response.
     2. Response body must follow **DiscoveredAPIs** data structure:
        * Check if DiscoveredAPIs contains previously registered Service APIs published.
  4. Response to Discover Request By Invoker:
     1. **404 Not Found** response.
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 404
        * title with message "Not Found"
        * detail with message "API Invoker {api_invoker_id} has no API Published that accomplish filter conditions".
        * cause with message "No API Published accomplish filter conditions".


## Test Case 6: Discover Published service APIs by registered API Invoker not filtered
* **Test ID**: ***capif_api_discover_service-6***
* **Description**:

  This test case will check if NetApp (Invoker) can discover published service APIs.
* **Pre-Conditions**:
  * 2 Service APIs are published.
  * NetApp was registered previously
  * NetApp was onboarded previously with {onboardingId}
  
* **Information of Test**:
  1. Perform [Provider Registration] and [Invoker Onboarding]
  2. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_1
     * Use APF Certificate
  3. Publish Service API at CCF:
     * Send Post to ccf_publish_url *https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis*
     * body [service api description] with apiName service_2
     * Use APF Certificate
  4.  Request Discover Published APIs not filtered:
     * Send GET to ccf_discover_url *https://{CAPIF_HOSTNAME}/service-apis/v1/allServiceAPIs?api-invoker-id={apiInvokerId}*
     * Param api-invoker-id is mandatory
     * Using invoker certificate

* **Execution Steps**:
  1. Register Provider at CCF, store certificates and Publish Service API service_1 and service_2 at CCF
  2. Register Invoker and Onboard Invoker at CCF
  3. Discover Service APIs by Invoker.
  4. Discover without filter by Invoker

* **Expected Result**:

  1. Response to Publish request must accomplish:
     1. **201 Created**
     2. Response Body must follow **ServiceAPIDescription** data structure with:
        * apiId
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/published-apis/v1/{apfId}/service-apis/{serviceApiId}*

  2. Response to Onboard request must accomplish:
     1. **201 Created**
     2. Response Body must follow **APIInvokerEnrolmentDetails** data structure with:
        * apiInvokerId
        * onboardingInformation->apiInvokerCertificate must contain the public key signed.
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/api-invoker-management/{apiVersion}/onboardedInvokers/{onboardingId}*

  3. Response to Discover Request By Invoker:
     1. **200 OK** response.
     2. Response body must follow **DiscoveredAPIs** data structure:
        * Check if DiscoveredAPIs contains the 2 previously registered Service APIs published.



   [service api description]: ./api_publish_service/service_api_description_post_example.json  "Service API **Description** Request"
   [publisher register body]: ./api_publish_service/publisher_register_body.json  "Publish register Body"
   [invoker onboarding body]: ../api_invoker_management/invoker_details_post_example.json  "API Invoker Request"
   [invoker register body]: ../api_invoker_management/invoker_register_body.json  "Invoker Register Body"
   [provider request body]: ../api_provider_management/provider_details_post_example.json  "API Provider Enrolment Request"
   [provider request patch body]: ../api_provider_management/provider_details_enrolment_details_patch_example.json  "API Provider Enrolment Patch Request"
   [provider getauth body]: ../api_provider_management/provider_getauth_example.json    "Get Auth Example"
   [invoker onboarding]: ../common_operations/README.md#register-an-invoker "Invoker Onboarding"
   [provider registration]: ../common_operations/README.md#register-a-provider "Provider Registration"


[Return To All Test Plans]: ../README.md
