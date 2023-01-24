[**[Return To All Test Plans]**]

- [Test Plan for CAPIF Api Events Service](#test-plan-for-capif-api-events-service)
- [Tests](#tests)
  - [Test Case 1: Creates a new individual CAPIF Event Subscription.](#test-case-1-creates-a-new-individual-capif-event-subscription)
  - [Test Case 2: Creates a new individual CAPIF Event Subscription with Invalid SubscriberId](#test-case-2-creates-a-new-individual-capif-event-subscription-with-invalid-subscriberid)
  - [Test Case 3: Deletes an individual CAPIF Event Subscription](#test-case-3-deletes-an-individual-capif-event-subscription)
  - [Test Case 4: Deletes an individual CAPIF Event Subscription with invalid SubscriberId](#test-case-4-deletes-an-individual-capif-event-subscription-with-invalid-subscriberid)
  - [Test Case 5: Deletes an individual CAPIF Event Subscription with invalid SubscriptionId](#test-case-5-deletes-an-individual-capif-event-subscription-with-invalid-subscriptionid)
 


# Test Plan for CAPIF Api Events Service
At this documentation you will have all information and related files and examples of test plan for this API.

# Tests

## Test Case 1: Creates a new individual CAPIF Event Subscription.
* Test ID: ***capif_api_events-1***
* Description:

  This test case will check that a CAPIF subscriber (Invoker or Publisher) can Subscribe to Events
* Pre-Conditions:
  
  * CAPIF subscriber is pre-authorised (has valid InvokerId or apfId from CAPIF Authority)

* Information of Test:

  1. Perform [Invoker Onboarding]

  2. Event Subscription:
     1. Send POST to *https://{CAPIF_HOSTNAME}/capif-events/v1/{subscriberId}/subscriptions*
     2. body [event subscription request body]
     3. Use Invoker Certificate

* Execution Steps:
  
  1. Register Invoker and Onboard Invoker at CCF
  2. Subscribe to Events
  3. Retrieve {subscriberId} and {subscriptionId} from Location Header
   
* Expected Result:

  1. Response to Onboard request must accomplish:
     1. **201 Created**
     2. Response Body must follow **APIInvokerEnrolmentDetails** data structure with:
        * apiInvokerId
        * onboardingInformation->apiInvokerCertificate must contain the public key signed.
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/api-invoker-management/{apiVersion}/onboardedInvokers/{onboardingId}*

  2. Response to Event Subscription must accomplish:
     1. **201 Created**
     2. The URI of the created resource shall be returned in the "Location" HTTP header, following this structure: *{apiRoot}/capif-events/{apiVersion}/{subscriberId}/subscriptions/{subscriptionId}
     3. Response Body must follow **EventSubscription** data structure.

  3. Event Subscriptions are stored in CAPIF Database


## Test Case 2: Creates a new individual CAPIF Event Subscription with Invalid SubscriberId
* Test ID: ***capif_api_events-2***
* Description:

  This test case will check that a CAPIF subscriber (Invoker or Publisher) cannot Subscribe to Events without valid SubcriberId
* Pre-Conditions:
  
  * CAPIF subscriber is not pre-authorised (has invalid InvokerId or apfId)

* Information of Test:

  1. Perform [Invoker Onboarding]

  2. Event Subscription:
     1. Send POST to *https://{CAPIF_HOSTNAME}/capif-events/v1/{SUBSCRIBER_NOT_REGISTERED}/subscriptions*
     2. body [event subscription request body]
     3. Use Invoker Certificate

* Execution Steps:
  
  1. Register Invoker and Onboard Invoker at CCF
  2. Subscribe to Events
   
* Expected Result:

  1. Response to Onboard request must accomplish:
     1. **201 Created**
     2. Response Body must follow **APIInvokerEnrolmentDetails** data structure with:
        * apiInvokerId
        * onboardingInformation->apiInvokerCertificate must contain the public key signed.
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/api-invoker-management/{apiVersion}/onboardedInvokers/{onboardingId}*

  2. Response to Event Subscription must accomplish:
     1. **404 Not Found**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 404
        * title with message "Not Found"
        * detail with message "Invoker or APF or AEF or AMF Not found".
        * cause with message "Subscriber Not Found".

  3. Event Subscriptions are not stored in CAPIF Database

  
## Test Case 3: Deletes an individual CAPIF Event Subscription
* Test ID: ***capif_api_events-3***
* Description:

  This test case will check that a CAPIF subscriber (Invoker or Publisher) can Delete an Event Subscription
* Pre-Conditions:
  
  * CAPIF subscriber is pre-authorised (has valid InvokerId or apfId from CAPIF Authority)

* Information of Test:

  1. Perform [Invoker Onboarding]

  2. Event Subscription:
     1. Send POST to *https://{CAPIF_HOSTNAME}/capif-events/v1/{subscriberId}/subscriptions*
     2. body [event subscription request body]
     3. Use Invoker Certificate

  3. Remove Event Subscription:
     1. Send DELETE to *https://{CAPIF_HOSTNAME}/capif-events/v1/{subscriberId}/subscriptions*
     2. Use Invoker Certificate

* Execution Steps:
  
  1. Register Invoker and Onboard Invoker at CCF
  2. Subscribe to Events
  3. Retrieve {subscriberId} and {subscriptionId} from Location Header
  4. Remove Event Subscription
   
* Expected Result:

  1. Response to Onboard request must accomplish:
     1. **201 Created**
     2. Response Body must follow **APIInvokerEnrolmentDetails** data structure with:
        * apiInvokerId
        * onboardingInformation->apiInvokerCertificate must contain the public key signed.
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/api-invoker-management/{apiVersion}/onboardedInvokers/{onboardingId}*

  2. Response to Event Subscription must accomplish:
     1. **201 Created**
     2. The URI of the created resource shall be returned in the "Location" HTTP header, following this structure: *{apiRoot}/capif-events/{apiVersion}/{subscriberId}/subscriptions/{subscriptionId}
     3. Response Body must follow **EventSubscription** data structure.

  3. Event Subscriptions are stored in CAPIF Database
  4. Remove Event Subscription:
     1. **204 No Content**

  5. Event Subscription is not present at CAPIF Database.


## Test Case 4: Deletes an individual CAPIF Event Subscription with invalid SubscriberId
* Test ID: ***capif_api_events-4***
* Description:

  This test case will check that a CAPIF subscriber (Invoker or Publisher) cannot Delete to Events without valid SubcriberId
* Pre-Conditions:
  
  * CAPIF subscriber is pre-authorised (has valid InvokerId or apfId).
  * CAPIF subscriber is subscribed to Events.

* Information of Test:

  1. Perform [Invoker Onboarding]

  2. Event Subscription:
     1. Send POST to https://{CAPIF_HOSTNAME}/capif-events/v1/{subscriberId}/subscriptions
     2. body [event subscription request body]
     3. Use Invoker Certificate

  3. Remove Event Subcription with not valid subscriber:
     1. Send DELETE to to https://{CAPIF_HOSTNAME}/capif-events/v1/{SUBSCRIBER_ID_NOT_VALID}/subscriptions/{subcriptionId}
     2. Use Invoker Certificate

* Execution Steps:
  
  1. Register Invoker and Onboard Invoker at CCF
  2. Subscribe to Events
  3. Retrieve Location Header with subscriptionId.
  4. Remove Event Subscribed with not valid Subscriber.
   
* Expected Result:

  1. Response to Onboard request must accomplish:
     1. **201 Created**
     2. Response Body must follow **APIInvokerEnrolmentDetails** data structure with:
        * apiInvokerId
        * onboardingInformation->apiInvokerCertificate must contain the public key signed.
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/api-invoker-management/{apiVersion}/onboardedInvokers/{onboardingId}*

  2. Response to Event Subscription must accomplish:
     1. 201 Created
     2. The URI of the created resource shall be returned in the "Location" HTTP header, following this structure: *{apiRoot}/capif-events/{apiVersion}/{subscriberId}/subscriptions/{subscriptionId}
     3. Response Body must follow **EventSubscription** data structure.

  3. Event Subscriptions are stored in CAPIF Database
  4. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 404
        * title with message "Not Found"
        * detail with message "Invoker or APF or AEF or AMF Not found".
        * cause with message "Subscriber Not Found".


## Test Case 5: Deletes an individual CAPIF Event Subscription with invalid SubscriptionId
* Test ID: ***capif_api_events-5***
* Description:

  This test case will check that a CAPIF subscriber (Invoker or Publisher) cannot Delete an Event Subscription without valid SubscriptionId
* Pre-Conditions:
  
  * CAPIF subscriber is pre-authorised (has invalid InvokerId or apfId).
  * CAPIF subscriber is subscribed to Events.

* Information of Test:

  1. Perform [Invoker Onboarding]

  2. Event Subscription:
     1. Send POST to https://{CAPIF_HOSTNAME}/capif-events/v1/{subscriberId}/subscriptions
     2. body [event subscription request body]
     3. Use Invoker Certificate

  3. Remove Event Subcription with not valid subscriber:
     1. Send DELETE to to https://{CAPIF_HOSTNAME}/capif-events/v1/{subcriberId}/subscriptions/{SUBSCRIPTION_ID_NOT_VALID}
     2. Use Invoker Certificate

* Execution Steps:
  
  1. Register Invoker and Onboard Invoker at CCF
  2. Subscribe to Events
  3. Retrieve Location Header with subscriptionId.
  4. Remove Event Subscribed with not valid Subscriber.
   
* Expected Result:

  1. Response to Onboard request must accomplish:
     1. **201 Created**
     2. Response Body must follow **APIInvokerEnrolmentDetails** data structure with:
        * apiInvokerId
        * onboardingInformation->apiInvokerCertificate must contain the public key signed.
     3. Response Header **Location** must be received with URI to new resource created, following this structure: *{apiRoot}/api-invoker-management/{apiVersion}/onboardedInvokers/{onboardingId}*

  2. Response to Event Subscription must accomplish:
     1. **201 Created**
     2. The URI of the created resource shall be returned in the "Location" HTTP header, following this structure: *{apiRoot}/capif-events/{apiVersion}/{subscriberId}/subscriptions/{subscriptionId}
     3. Response Body must follow **EventSubscription** data structure.

  3. Event Subscriptions are stored in CAPIF Database
  4. Remove Event Subscription with not valid subscriber:
     1. **404 Not Found**
     2. Error Response Body must accomplish with **ProblemDetails** data structure with:
        * status 404
        * detail with message "Service API not existing".
        * cause with message "Event API subscription id not found".




[invoker register body]: ../api_invoker_management/invoker_register_body.json  "Invoker Register Body"
[invoker onboard request body]: ../api_invoker_management/invoker_details_post_example.json  "API Invoker Request"
[event subscription request body]: ./event_subscription.json  "Event Subscription Request"
[invoker onboarding]: ../common_operations/README.md#register-an-invoker "Invoker Onboarding"


[Return To All Test Plans]: ../README.md
