[**[Return To All Test Plans]**]

- [Test Plan for CAPIF Api Logging Service](#test-plan-for-capif-api-logging-service)
- [Tests](#tests)
  - [Test Case 1: Creates a new individual CAPIF Log Entry.](#test-case-1-creates-a-new-individual-capif-log-entry)
  - [Test Case 2: Creates a new individual CAPIF Log Entry with Invalid aefID](#test-case-2-creates-a-new-individual-capif-log-entry-with-invalid-aefid)
  - [Test Case 3: Creates a new individual CAPIF Log Entry with Invalid serviceAPI](#test-case-3-creates-a-new-individual-capif-log-entry-with-invalid-serviceapi)
  - [Test Case 4: Creates a new individual CAPIF Log Entry with Invalid apiInvokerId](#test-case-4-creates-a-new-individual-capif-log-entry-with-invalid-apiinvokerid)

  - [Test Case 5: Creates a new individual CAPIF Log Entry with differnted aef_id in body and request](#test-case-5-creates-a-new-individual-capif-log-entry-with-invalid-aefid-in-body)


# Test Plan for CAPIF Api Logging Service
At this documentation you will have all information and related files and examples of test plan for this API.

# Tests

## Test Case 1: Creates a new individual CAPIF Log Entry.
* Test ID: ***capif_api_logging-1***
* Description:

  This test case will check that a CAPIF AEF can create log entry to Logging Service
* Pre-Conditions:
  
  *  CAPIF provider is pre-authorised (has valid aefId from CAPIF Authority)
  *  Service exist in CAPIF
  *  Invoker exist in CAPIF

* Information of Test:

  1. Perform [provider onboarding] and [invoker onboarding]

  2. Publish Service API at CCF:
    - Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
    - body [service api description] with apiName service_1
    - Use APF Certificate

  3. Log Entry:
     1. Send POST to *https://{CAPIF_HOSTNAME}/api-invocation-logs/v1/{aefId}/logs*
     2. body [log entry request body]
     3. Use AEF Certificate

* Execution Steps:
  1. Register Provider and Invoker CCF
  2. Publish Service
  3. Create Log Entry

* Expected Result:

  1. Response to Logging Service must accomplish:
     1. **201 Created**
     2. Response Body must follow **InvocationLog** data structure with:
        * aefId
        * apiInvokerId
        * logs
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/api-invocation-logs/v1/{aefId}/logs/{logId}*




## Test Case 2:  Creates a new individual CAPIF Log Entry with Invalid aefId
* Test ID: ***capif_api_logging-2***
* Description:

  This test case will check that a CAPIF subscriber (AEF) cannot create Log Entry without valid aefId
* Pre-Conditions:

  * CAPIF provider is not pre-authorised (has not valid aefId from CAPIF Authority)
  *  Service exist in CAPIF
  *  Invoker exist in CAPIF

* Information of Test:

  1. Perform [provider onboarding] and [invoker onboarding]

  2. Publish Service API at CCF:
    - Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
    - body [service api description] with apiName service_1
    - Use APF Certificate

  3. Log Entry:
     1. Send POST to *https://{CAPIF_HOSTNAME}/api-invocation-logs/v1/{not-valid-aefId}/logs*
     2. body [log entry request body]
     3. Use AEF Certificate

* Execution Steps:
  1. Register Provider and Invoker CCF
  2. Publish Service
  3. Create Log Entry
   
* Expected Result:

  1. Response to Logging Service must accomplish:
     1. **404 Not Found**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 404
        * title with message "Not Found"
        * detail with message "Exposer not exist".
        * cause with message "Exposer id not found".

## Test Case 3:  Creates a new individual CAPIF Log Entry with Invalid serviceAPI
* Test ID: ***capif_api_logging-3***
* Description:

  This test case will check that a CAPIF subscriber (AEF) cannot create Log Entry without valid aefId
* Pre-Conditions:
  
  * CAPIF subscriber is pre-authorised (has valid aefId from CAPIF Authority)

* Information of Test:

  1. Perform [provider onboarding] and [invoker onboarding]

  2. Publish Service API at CCF:
    - Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
    - body [service api description] with apiName service_1
    - Use APF Certificate

  3. Log Entry:
     1. Send POST to *https://{CAPIF_HOSTNAME}/api-invocation-logs/v1/{aefId}/logs*
     2. body [log entry request body with serviceAPI apiName apiId not valid]
     3. Use AEF Certificate

* Execution Steps:
  1. Register Provider and Invoker CCF
  2. Publish Service
  3. Create Log Entry

* Expected Result:

  1. Response to Logging Service must accomplish:
     1. **404 Not Found**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 404
        * title with message "Not Found"
        * detail with message "Invoker not exist".
        * cause with message "Invoker id not found".



## Test Case 4:  Creates a new individual CAPIF Log Entry with Invalid apiInvokerId
* Test ID: ***capif_api_logging-4***
* Description:

  This test case will check that a CAPIF subscriber (AEF) cannot create Log Entry without valid aefId
* Pre-Conditions:
  
  * CAPIF subscriber is pre-authorised (has valid aefId from CAPIF Authority)

* Information of Test:

  1. Perform [provider onboarding] and [invoker onboarding]

  2. Publish Service API at CCF:
    - Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
    - body [service api description] with apiName service_1
    - Use APF Certificate

  3. Log Entry:
     1. Send POST to *https://{CAPIF_HOSTNAME}/api-invocation-logs/v1/{aefId}/logs*
     2. body [log entry request body with invokerId not valid]
     3. Use AEF Certificate

* Execution Steps:
  1. Register Provider and Invoker CCF
  2. Publish Service
  3. Create Log Entry
   
* Expected Result:

  1. Response to Onboard request must accomplish:
     1. **201 Created** response.
     2. body returned must accomplish **APIProviderEnrolmentDetails** data structure.
     3. For each **apiProvFuncs**, we must check:
        1. **apiProvFuncId** is set
        2. **apiProvCert** under **regInfo** is set properly
     5. Location Header must contain the new resource URL *{apiRoot}/api-provider-management/v1/registrations/{registrationId}*

  2. Response to Logging Service must accomplish:
     1. **404 Not Found**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 404
        * title with message "Not Found"
        * detail with message "Invoker not exist".
        * cause with message "Invoker id not found".

  3. Log Entry are not stored in CAPIF Database


## Test Case 5:  Creates a new individual CAPIF Log Entry with Invalid aefId in body
* Test ID: ***capif_api_logging-5***
* Description:

  This test case will check that a CAPIF subscriber (AEF) cannot create Log Entry without valid aefId in body
* Pre-Conditions:

  *  CAPIF provider is pre-authorised (has valid apfId from CAPIF Authority)
  *  Service exist in CAPIF
  *  Invoker exist in CAPIF

* Information of Test:

  1. Perform [provider onboarding] and [invoker onboarding]

  2. Publish Service API at CCF:
    - Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
    - body [service api description] with apiName service_1
    - Use APF Certificate

  3. Log Entry:
     1. Send POST to *https://{CAPIF_HOSTNAME}/api-invocation-logs/v1/{aefId}/logs*
     2. body [log entry request body with bad aefId] 
     3. Use AEF Certificate

* Execution Steps:
  1. Register Provider and Invoker CCF
  2. Publish Service
  3. Create Log Entry
  
* Expected Result:

  1. Response to Logging Service must accomplish:
     1. **401 Unauthorized**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 401
        * title with message "Unauthorized"
        * detail with message "AEF id not matching in request and body".
        * cause with message "Not identical AEF id".






[log entry request body]: ./invocation_log.json "Log Request Body"

[invoker onboarding]: ../common_operations/README.md#register-an-invoker "Invoker Onboarding"

[provider onboarding]: ../common_operations/README.md#register-a-provider "Provider Onboarding"

[Return To All Test Plans]: ../README.md
