# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from capif_security.models.access_token_err import AccessTokenErr  # noqa: E501
from capif_security.models.access_token_rsp import AccessTokenRsp  # noqa: E501
from capif_security.models.problem_details import ProblemDetails  # noqa: E501
from capif_security.models.security_notification import SecurityNotification  # noqa: E501
from capif_security.models.service_security import ServiceSecurity  # noqa: E501
from capif_security.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    @unittest.skip("application/x-www-form-urlencoded not supported by Connexion")
    def test_securities_security_id_token_post(self):
        """Test case for securities_security_id_token_post

        
        """
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = dict(grant_type='grant_type_example',
                    client_id='client_id_example',
                    client_secret='client_secret_example',
                    scope='scope_example')
        response = self.client.open(
            '/capif-security/v1/securities/{security_id}/token'.format(security_id='security_id_example'),
            method='POST',
            headers=headers,
            data=data,
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_trusted_invokers_api_invoker_id_delete(self):
        """Test case for trusted_invokers_api_invoker_id_delete

        
        """
        headers = { 
            'Accept': 'application/problem+json',
        }
        response = self.client.open(
            '/capif-security/v1/trustedInvokers/{api_invoker_id}'.format(api_invoker_id='api_invoker_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_trusted_invokers_api_invoker_id_delete_post(self):
        """Test case for trusted_invokers_api_invoker_id_delete_post

        
        """
        security_notification = {
  "apiInvokerId" : "apiInvokerId",
  "aefId" : "aefId",
  "apiIds" : [ "apiIds", "apiIds" ]
}
        headers = { 
            'Accept': 'application/problem+json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/capif-security/v1/trustedInvokers/{api_invoker_id}/delete'.format(api_invoker_id='api_invoker_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(security_notification),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_trusted_invokers_api_invoker_id_get(self):
        """Test case for trusted_invokers_api_invoker_id_get

        
        """
        query_string = [('authenticationInfo', True),
                        ('authorizationInfo', True)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/capif-security/v1/trustedInvokers/{api_invoker_id}'.format(api_invoker_id='api_invoker_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_trusted_invokers_api_invoker_id_put(self):
        """Test case for trusted_invokers_api_invoker_id_put

        
        """
        service_security = {
  "notificationDestination" : "notificationDestination",
  "supportedFeatures" : "supportedFeatures",
  "securityInfo" : [ {
    "authenticationInfo" : "authenticationInfo",
    "authorizationInfo" : "authorizationInfo",
    "interfaceDetails" : {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 5248,
      "ipv4Addr" : "ipv4Addr"
    },
    "prefSecurityMethods" : [ null, null ],
    "aefId" : "aefId"
  }, {
    "authenticationInfo" : "authenticationInfo",
    "authorizationInfo" : "authorizationInfo",
    "interfaceDetails" : {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 5248,
      "ipv4Addr" : "ipv4Addr"
    },
    "prefSecurityMethods" : [ null, null ],
    "aefId" : "aefId"
  } ],
  "websockNotifConfig" : {
    "requestWebsocketUri" : true,
    "websocketUri" : "websocketUri"
  },
  "requestTestNotification" : true
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/capif-security/v1/trustedInvokers/{api_invoker_id}'.format(api_invoker_id='api_invoker_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(service_security),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_trusted_invokers_api_invoker_id_update_post(self):
        """Test case for trusted_invokers_api_invoker_id_update_post

        
        """
        service_security = {
  "notificationDestination" : "notificationDestination",
  "supportedFeatures" : "supportedFeatures",
  "securityInfo" : [ {
    "authenticationInfo" : "authenticationInfo",
    "authorizationInfo" : "authorizationInfo",
    "interfaceDetails" : {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 5248,
      "ipv4Addr" : "ipv4Addr"
    },
    "prefSecurityMethods" : [ null, null ],
    "aefId" : "aefId"
  }, {
    "authenticationInfo" : "authenticationInfo",
    "authorizationInfo" : "authorizationInfo",
    "interfaceDetails" : {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 5248,
      "ipv4Addr" : "ipv4Addr"
    },
    "prefSecurityMethods" : [ null, null ],
    "aefId" : "aefId"
  } ],
  "websockNotifConfig" : {
    "requestWebsocketUri" : true,
    "websocketUri" : "websocketUri"
  },
  "requestTestNotification" : true
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/capif-security/v1/trustedInvokers/{api_invoker_id}/update'.format(api_invoker_id='api_invoker_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(service_security),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
