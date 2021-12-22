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
  
  This test case will check that a CAPIF subscriber (Invoker or Publisher) can Subscribe to Events 

* Pre-Conditions: 
  
  CAPIF subscriber is pre-authorised (has valid InvvokerId or apfId from CAPIF Authority) 

* Actions:

  POST Event Subscription
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  Event Subscriptions are stored in CAPIF Database

  201 Created (Successful creation of subscription) 

  Events API subscribed successfully The URI of the created resource shall be returned in the "Location" HTTP header. 

  Location Contains the URI of the newly created resource, according to the structure: {apiRoot}/capif-events/v1/{subscriberId}/subscriptions/{subscriptionId}

## Test Case 2: Creates a new individual CAPIF Event Subscription with Invalid SubscriberId
  
  This test case will check that a CAPIF subscriber (Invoker or Publisher) cannot Subscribe to Events without valid SubcribeId

* Pre-Conditions: 
  
  CAPIF subscriber is not pre-authorised (has invalid InvvokerId or apfId) 

* Actions:

  POST Event Subscription
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  Event Subscriptions are not stored in CAPIF Database

  403 Forbidden
  
## Test Case 3: Deletes an individual CAPIF Event Subscription
  
  This test case will check that a CAPIF subscriber (Invoker or Publisher) can Delete an Event Subscrioption

* Pre-Conditions: 
  
  CAPIF subscriber is pre-authorised (has valid InvvokerId or apfId)  

* Actions:

  DELETE Event Subscription
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  Event Subscription with SubscriptionId is deleted from CAPIF Database

  204 The individual CAPIF Events Subscription matching the subscriptionId is deleted.

## Test Case 4: Deletes an individual CAPIF Event Subscription with invalid SubscriberId
  
  This test case will check that a CAPIF subscriber (Invoker or Publisher) cannot Delete an Event Subscrioption without valid SubscriberId

* Pre-Conditions: 
  
  CAPIF subscriber is not pre-authorised (has invalid InvvokerId or apfId) 

* Actions:

  DELETE Event Subscription
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  Event Subscription with SubscriptionId is not deleted from CAPIF Database

  403 Forbidden

## Test Case 5: Deletes an individual CAPIF Event Subscription with invalid SubscriptionId
  
  This test case will check that a CAPIF subscriber (Invoker or Publisher) cannot Delete an Event Subscrioption without valid SubscriptionId

* Pre-Conditions: 
  
  CAPIF subscriber is pre-authorised (has valid InvvokerId or apfId) but Event to delete has invalid SubscriptionId
  
* Actions:

  DELETE Event Subscription
    
  Request Body: [request body](tc1_post_body_example.json)

* Post-Conditions:
  
  404 Not Found

