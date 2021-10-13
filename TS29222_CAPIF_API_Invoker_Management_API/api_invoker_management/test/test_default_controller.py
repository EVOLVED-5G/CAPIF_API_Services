# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api_invoker_management.models.api_invoker_enrolment_details import APIInvokerEnrolmentDetails  # noqa: E501
from api_invoker_management.models.problem_details import ProblemDetails  # noqa: E501
from api_invoker_management.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_onboarded_invokers_onboarding_id_delete(self):
        """Test case for onboarded_invokers_onboarding_id_delete

        
        """
        headers = { 
            'Accept': 'application/problem+json',
        }
        response = self.client.open(
            '/api-invoker-management/v1/onboardedInvokers/{onboarding_id}'.format(onboarding_id='onboarding_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_onboarded_invokers_onboarding_id_put(self):
        """Test case for onboarded_invokers_onboarding_id_put

        
        """
        api_invoker_enrolment_details = {
  "notificationDestination" : "notificationDestination",
  "supportedFeatures" : "supportedFeatures",
  "apiInvokerId" : "apiInvokerId",
  "apiInvokerInformation" : "apiInvokerInformation",
  "websockNotifConfig" : {
    "requestWebsocketUri" : true,
    "websocketUri" : "websocketUri"
  },
  "onboardingInformation" : {
    "apiInvokerPublicKey" : "apiInvokerPublicKey",
    "onboardingSecret" : "onboardingSecret",
    "apiInvokerCertificate" : "apiInvokerCertificate"
  },
  "requestTestNotification" : true,
  "apiList" : [ {
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
  }, {
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
  } ]
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api-invoker-management/v1/onboardedInvokers/{onboarding_id}'.format(onboarding_id='onboarding_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(api_invoker_enrolment_details),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_onboarded_invokers_post(self):
        """Test case for onboarded_invokers_post

        
        """
        api_invoker_enrolment_details = {
  "notificationDestination" : "notificationDestination",
  "supportedFeatures" : "supportedFeatures",
  "apiInvokerId" : "apiInvokerId",
  "apiInvokerInformation" : "apiInvokerInformation",
  "websockNotifConfig" : {
    "requestWebsocketUri" : true,
    "websocketUri" : "websocketUri"
  },
  "onboardingInformation" : {
    "apiInvokerPublicKey" : "apiInvokerPublicKey",
    "onboardingSecret" : "onboardingSecret",
    "apiInvokerCertificate" : "apiInvokerCertificate"
  },
  "requestTestNotification" : true,
  "apiList" : [ {
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
  }, {
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
  } ]
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api-invoker-management/v1/onboardedInvokers',
            method='POST',
            headers=headers,
            data=json.dumps(api_invoker_enrolment_details),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
