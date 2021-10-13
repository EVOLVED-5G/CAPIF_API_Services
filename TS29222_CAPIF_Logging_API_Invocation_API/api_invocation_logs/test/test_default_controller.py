# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api_invocation_logs.models.invocation_log import InvocationLog  # noqa: E501
from api_invocation_logs.models.problem_details import ProblemDetails  # noqa: E501
from api_invocation_logs.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_aef_id_logs_post(self):
        """Test case for aef_id_logs_post

        
        """
        invocation_log = {
  "supportedFeatures" : "supportedFeatures",
  "apiInvokerId" : "apiInvokerId",
  "aefId" : "aefId",
  "logs" : [ {
    "apiName" : "apiName",
    "invocationTime" : "2000-01-23T04:56:07.000+00:00",
    "srcInterface" : {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 39500,
      "ipv4Addr" : "ipv4Addr"
    },
    "fwdInterface" : "fwdInterface",
    "resourceName" : "resourceName",
    "uri" : "uri",
    "inputParameters" : "",
    "invocationLatency" : 0,
    "result" : "result",
    "apiVersion" : "apiVersion",
    "destInterface" : {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 39500,
      "ipv4Addr" : "ipv4Addr"
    },
    "apiId" : "apiId",
    "outputParameters" : ""
  }, {
    "apiName" : "apiName",
    "invocationTime" : "2000-01-23T04:56:07.000+00:00",
    "srcInterface" : {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 39500,
      "ipv4Addr" : "ipv4Addr"
    },
    "fwdInterface" : "fwdInterface",
    "resourceName" : "resourceName",
    "uri" : "uri",
    "inputParameters" : "",
    "invocationLatency" : 0,
    "result" : "result",
    "apiVersion" : "apiVersion",
    "destInterface" : {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 39500,
      "ipv4Addr" : "ipv4Addr"
    },
    "apiId" : "apiId",
    "outputParameters" : ""
  } ]
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api-invocation-logs/v1/{aef_id}/logs'.format(aef_id='aef_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(invocation_log),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
