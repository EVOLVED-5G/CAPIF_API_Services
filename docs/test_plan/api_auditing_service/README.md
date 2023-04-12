[**[Return To All Test Plans]**]

- [Test Plan for CAPIF Api Auditing Service](#test-plan-for-capif-api-auditing-service)
- [Tests](#tests)
  - [Test Case 1: Get a CAPIF Log Entry.](#test-case-1-creates-a-new-individual-capif-log-entry)


# Test Plan for CAPIF Api Auditing Service
At this documentation you will have all information and related files and examples of test plan for this API.

# Tests

## Test Case 1: Get CAPIF Log Entry.
* Test ID: ***capif_api_auditing-1***
* Description:

  This test case will check that a CAPIF AMF can get log entry to Logging Service
* Pre-Conditions:
  
  *  CAPIF provider is pre-authorised (has valid AMF cert from CAPIF Authority)
  *  Service exist in CAPIF
  *  Invoker exist in CAPIF
  *  Log Entry exist in CAPIF

* Information of Test:

  1. Perform [provider onboarding], [invoker onboarding] 

  2. Publish Service API at CCF:
    - Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
    - body [service api description] with apiName service_1
    - Use APF Certificate

  3. Create Log Entry:
     - Send POST to *https://{CAPIF_HOSTNAME}/api-invocation-logs/v1/{aefId}/logs*
     - body [log entry request body]
     - Use AEF Certificate

  4. Get Log:
     1. Send GET to *https://{CAPIF_HOSTNAME}/logs/v1/apiInvocationLogs?aef-id={aefId}&api-invoker-id={api-invoker-id}*
     2. Use AMF Certificate

* Execution Steps:
  1. Register Provider and Invoker CCF
  2. Publish Service
  3. Create Log Entry
  4. Get Log Entry

* Expected Result:

  1. Response to Logging Service must accomplish:
     1. **200 OK**
     2. Response Body must follow **InvocationLog** data structure with:
        * aefId
        * apiInvokerId
        * logs

## Test Case 2: Get CAPIF Log Entry With no Log entry in CAPIF.
* Test ID: ***capif_api_auditing-2***
* Description:

  This test case will check that a CAPIF AEF can create log entry to Logging Service
* Pre-Conditions:

  *  CAPIF provider is pre-authorised (has valid AMF cert from CAPIF Authority)
  *  Service exist in CAPIF
  *  Invoker exist in CAPIF


* Information of Test:

  1. Perform [provider onboarding], [invoker onboarding] 

  2. Publish Service API at CCF:
    - Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
    - body [service api description] with apiName service_1
    - Use APF Certificate

  4. Get Log:
     1. Send GET to *https://{CAPIF_HOSTNAME}/logs/v1/apiInvocationLogs?aef-id={aefId}&api-invoker-id={api-invoker-id}*
     2. Use AMF Certificate

* Execution Steps:
  1. Register Provider and Invoker CCF
  2. Publish Service
  3. Get Log Entry

* Expected Result:

  1. Response to Logging Service must accomplish:
     1. **404 Not Found**
    2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 404
        * title with message "Not Found Log Entry in CAPIF".
        * cause with message "Not Exist Logs with the filters applied".


## Test Case 3: Get CAPIF Log Entry without aef-id and api-invoker-id.
* Test ID: ***capif_api_auditing-3***
* Description:

  This test case will check that a CAPIF AEF can create log entry to Logging Service
* Pre-Conditions:

  *  CAPIF provider is no pre-authorised (has no valid AMF cert from CAPIF Authority)
  *  Service exist in CAPIF
  *  Invoker exist in CAPIF
  *  Log Entry exist in CAPIF

* Information of Test:

  1. Perform [provider onboarding], [invoker onboarding] 

  2. Publish Service API at CCF:
    - Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
    - body [service api description] with apiName service_1
    - Use APF Certificate

  3. Create Log Entry:
     - Send POST to *https://{CAPIF_HOSTNAME}/api-invocation-logs/v1/{aefId}/logs*
     - body [log entry request body]
     - Use AEF Certificate

  4. Get Log:
     1. Send GET to *https://{CAPIF_HOSTNAME}/logs/v1/apiInvocationLogs
     2. Use AMF Certificate

* Execution Steps:
  1. Register Provider and Invoker CCF
  2. Publish Service
  3. Create Log Entry
  4. Get Log Entry

* Expected Result:

  1. Response to Logging Service must accomplish:
     1. **400 Bad Request**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 400
        * title with message "Bad Request"
        * detail with message "aef_id and api_invoker_id parameters are mandatory".
        * cause with message "Mandatory parameters missing".


## Test Case 4: Get CAPIF Log Entry with filtter api-version.
* Test ID: ***capif_api_auditing-4***
* Description:

  This test case will check that a CAPIF AMF can get log entry to Logging Service
* Pre-Conditions:

  *  CAPIF provider is pre-authorised (has valid AMF cert from CAPIF Authority)
  *  Service exist in CAPIF
  *  Invoker exist in CAPIF
  *  Log Entry exist in CAPIF

* Information of Test:

  1. Perform [provider onboarding], [invoker onboarding] 

  2. Publish Service API at CCF:
    - Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
    - body [service api description] with apiName service_1
    - Use APF Certificate

  3. Create Log Entry:
     - Send POST to *https://{CAPIF_HOSTNAME}/api-invocation-logs/v1/{aefId}/logs*
     - body [log entry request body]
     - Use AEF Certificate

  4. Get Log:
     1. Send GET to *https://{CAPIF_HOSTNAME}/logs/v1/apiInvocationLogs?aef-id={aefId}&api-invoker-id={api-invoker-id}&api-version={v1}*
     2. Use AMF Certificate

* Execution Steps:
  1. Register Provider and Invoker CCF
  2. Publish Service
  3. Create Log Entry
  4. Get Log Entry

* Expected Result:

  1. Response to Logging Service must accomplish:
     1. **200 OK**
     2. Response Body must follow **InvocationLog** data structure with:
        * aefId
        * apiInvokerId
        * logs


## Test Case 5: Get CAPIF Log Entry with filter api-version but not exist in log entry.
* Test ID: ***capif_api_auditing-4***
* Description:

  This test case will check that a CAPIF AMF can get log entry to Logging Service
* Pre-Conditions:

  *  CAPIF provider is pre-authorised (has valid AMF cert from CAPIF Authority)
  *  Service exist in CAPIF
  *  Invoker exist in CAPIF
  *  Log Entry exist in CAPIF

* Information of Test:

  1. Perform [provider onboarding], [invoker onboarding] 

  2. Publish Service API at CCF:
    - Send Post to ccf_publish_url https://{CAPIF_HOSTNAME}/published-apis/v1/{apfId}/service-apis
    - body [service api description] with apiName service_1
    - Use APF Certificate

  3. Create Log Entry:
     - Send POST to *https://{CAPIF_HOSTNAME}/api-invocation-logs/v1/{aefId}/logs*
     - body [log entry request body]
     - Use AEF Certificate

  4. Get Log:
     1. Send GET to *https://{CAPIF_HOSTNAME}/logs/v1/apiInvocationLogs?aef-id={aefId}&api-invoker-id={api-invoker-id}&api-version={v58}*
     2. Use AMF Certificate

* Execution Steps:
  1. Register Provider and Invoker CCF
  2. Publish Service
  3. Create Log Entry
  4. Get Log Entry

* Expected Result:

  1. Response to Logging Service must accomplish:
     1. **404 Not Found**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 404
        * detail with message "Parameters do not match any log entry"
        * cause with message "No logs found".



[log entry request body]: ../api_logging_service/invocation_log.json "Log Request Body"

[invoker onboarding]: ../common_operations/README.md#register-an-invoker "Invoker Onboarding"

[provider onboarding]: ../common_operations/README.md#register-a-provider "Provider Onboarding"

[Return To All Test Plans]: ../README.md