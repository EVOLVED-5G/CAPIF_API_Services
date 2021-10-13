# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from capif_events.models.event_subscription import EventSubscription  # noqa: E501
from capif_events.models.problem_details import ProblemDetails  # noqa: E501
from capif_events.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_subscriber_id_subscriptions_post(self):
        """Test case for subscriber_id_subscriptions_post

        
        """
        event_subscription = {
  "notificationDestination" : "notificationDestination",
  "eventFilters" : [ {
    "aefIds" : [ "aefIds", "aefIds" ],
    "apiInvokerIds" : [ "apiInvokerIds", "apiInvokerIds" ],
    "apiIds" : [ "apiIds", "apiIds" ]
  }, {
    "aefIds" : [ "aefIds", "aefIds" ],
    "apiInvokerIds" : [ "apiInvokerIds", "apiInvokerIds" ],
    "apiIds" : [ "apiIds", "apiIds" ]
  } ],
  "supportedFeatures" : "supportedFeatures",
  "eventReq" : {
    "partitionCriteria" : [ null, null ],
    "grpRepTime" : 5,
    "monDur" : "2000-01-23T04:56:07.000+00:00",
    "immRep" : true,
    "maxReportNbr" : 0,
    "repPeriod" : 6,
    "sampRatio" : 15
  },
  "websockNotifConfig" : {
    "requestWebsocketUri" : true,
    "websocketUri" : "websocketUri"
  },
  "events" : [ null, null ],
  "requestTestNotification" : true
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/capif-events/v1/{subscriber_id}/subscriptions'.format(subscriber_id='subscriber_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(event_subscription),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_subscriber_id_subscriptions_subscription_id_delete(self):
        """Test case for subscriber_id_subscriptions_subscription_id_delete

        
        """
        headers = { 
            'Accept': 'application/problem+json',
        }
        response = self.client.open(
            '/capif-events/v1/{subscriber_id}/subscriptions/{subscription_id}'.format(subscriber_id='subscriber_id_example', subscription_id='subscription_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
