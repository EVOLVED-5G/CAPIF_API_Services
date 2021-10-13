# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from published_apis.models.problem_details import ProblemDetails  # noqa: E501
from published_apis.models.service_api_description import ServiceAPIDescription  # noqa: E501
from published_apis.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_apf_id_service_apis_get(self):
        """Test case for apf_id_service_apis_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/published-apis/v1/{apf_id}/service-apis'.format(apf_id='apf_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_apf_id_service_apis_post(self):
        """Test case for apf_id_service_apis_post

        
        """
        service_api_description = {
  "serviceAPICategory" : "serviceAPICategory",
  "ccfId" : "ccfId",
  "apiName" : "apiName",
  "shareableInfo" : {
    "capifProvDoms" : [ "capifProvDoms", "capifProvDoms" ],
    "isShareable" : true
  },
  "supportedFeatures" : "supportedFeatures",
  "description" : "description",
  "apiSuppFeats" : "apiSuppFeats",
  "apiId" : "apiId",
  "aefProfiles" : [ {
    "securityMethods" : [ null, null ],
    "versions" : [ {
      "apiVersion" : "apiVersion",
      "resources" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      } ],
      "custOperations" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      } ],
      "expiry" : "2000-01-23T04:56:07.000+00:00"
    }, {
      "apiVersion" : "apiVersion",
      "resources" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      } ],
      "custOperations" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      } ],
      "expiry" : "2000-01-23T04:56:07.000+00:00"
    } ],
    "domainName" : "domainName",
    "aefId" : "aefId",
    "interfaceDescriptions" : [ {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 5248,
      "ipv4Addr" : "ipv4Addr"
    }, {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 5248,
      "ipv4Addr" : "ipv4Addr"
    } ]
  }, {
    "securityMethods" : [ null, null ],
    "versions" : [ {
      "apiVersion" : "apiVersion",
      "resources" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      } ],
      "custOperations" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      } ],
      "expiry" : "2000-01-23T04:56:07.000+00:00"
    }, {
      "apiVersion" : "apiVersion",
      "resources" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      } ],
      "custOperations" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      } ],
      "expiry" : "2000-01-23T04:56:07.000+00:00"
    } ],
    "domainName" : "domainName",
    "aefId" : "aefId",
    "interfaceDescriptions" : [ {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 5248,
      "ipv4Addr" : "ipv4Addr"
    }, {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 5248,
      "ipv4Addr" : "ipv4Addr"
    } ]
  } ],
  "pubApiPath" : {
    "ccfIds" : [ "ccfIds", "ccfIds" ]
  }
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/published-apis/v1/{apf_id}/service-apis'.format(apf_id='apf_id_example'),
            method='POST',
            headers=headers,
            data=json.dumps(service_api_description),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_apf_id_service_apis_service_api_id_delete(self):
        """Test case for apf_id_service_apis_service_api_id_delete

        
        """
        headers = { 
            'Accept': 'application/problem+json',
        }
        response = self.client.open(
            '/published-apis/v1/{apf_id}/service-apis/{service_api_id}'.format(service_api_id='service_api_id_example', apf_id='apf_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_apf_id_service_apis_service_api_id_get(self):
        """Test case for apf_id_service_apis_service_api_id_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/published-apis/v1/{apf_id}/service-apis/{service_api_id}'.format(service_api_id='service_api_id_example', apf_id='apf_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_apf_id_service_apis_service_api_id_put(self):
        """Test case for apf_id_service_apis_service_api_id_put

        
        """
        service_api_description = {
  "serviceAPICategory" : "serviceAPICategory",
  "ccfId" : "ccfId",
  "apiName" : "apiName",
  "shareableInfo" : {
    "capifProvDoms" : [ "capifProvDoms", "capifProvDoms" ],
    "isShareable" : true
  },
  "supportedFeatures" : "supportedFeatures",
  "description" : "description",
  "apiSuppFeats" : "apiSuppFeats",
  "apiId" : "apiId",
  "aefProfiles" : [ {
    "securityMethods" : [ null, null ],
    "versions" : [ {
      "apiVersion" : "apiVersion",
      "resources" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      } ],
      "custOperations" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      } ],
      "expiry" : "2000-01-23T04:56:07.000+00:00"
    }, {
      "apiVersion" : "apiVersion",
      "resources" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      } ],
      "custOperations" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      } ],
      "expiry" : "2000-01-23T04:56:07.000+00:00"
    } ],
    "domainName" : "domainName",
    "aefId" : "aefId",
    "interfaceDescriptions" : [ {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 5248,
      "ipv4Addr" : "ipv4Addr"
    }, {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 5248,
      "ipv4Addr" : "ipv4Addr"
    } ]
  }, {
    "securityMethods" : [ null, null ],
    "versions" : [ {
      "apiVersion" : "apiVersion",
      "resources" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      } ],
      "custOperations" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      } ],
      "expiry" : "2000-01-23T04:56:07.000+00:00"
    }, {
      "apiVersion" : "apiVersion",
      "resources" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "resourceName" : "resourceName",
        "custOpName" : "custOpName",
        "uri" : "uri"
      } ],
      "custOperations" : [ {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      }, {
        "operations" : [ null, null ],
        "description" : "description",
        "custOpName" : "custOpName"
      } ],
      "expiry" : "2000-01-23T04:56:07.000+00:00"
    } ],
    "domainName" : "domainName",
    "aefId" : "aefId",
    "interfaceDescriptions" : [ {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 5248,
      "ipv4Addr" : "ipv4Addr"
    }, {
      "ipv6Addr" : "ipv6Addr",
      "securityMethods" : [ null, null ],
      "port" : 5248,
      "ipv4Addr" : "ipv4Addr"
    } ]
  } ],
  "pubApiPath" : {
    "ccfIds" : [ "ccfIds", "ccfIds" ]
  }
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/published-apis/v1/{apf_id}/service-apis/{service_api_id}'.format(service_api_id='service_api_id_example', apf_id='apf_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(service_api_description),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
