# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api_provider_management.models.api_provider_enrolment_details import APIProviderEnrolmentDetails  # noqa: E501
from api_provider_management.models.problem_details import ProblemDetails  # noqa: E501
from api_provider_management.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_registrations_post(self):
        """Test case for registrations_post

        
        """
        api_provider_enrolment_details = {
  "regSec" : "regSec",
  "apiProvFuncs" : [ {
    "apiProvFuncId" : "apiProvFuncId",
    "apiProvFuncInfo" : "apiProvFuncInfo",
    "regInfo" : {
      "apiProvCert" : "apiProvCert",
      "apiProvPubKey" : "apiProvPubKey"
    }
  }, {
    "apiProvFuncId" : "apiProvFuncId",
    "apiProvFuncInfo" : "apiProvFuncInfo",
    "regInfo" : {
      "apiProvCert" : "apiProvCert",
      "apiProvPubKey" : "apiProvPubKey"
    }
  } ],
  "failReason" : "failReason",
  "apiProvDomId" : "apiProvDomId",
  "apiProvDomInfo" : "apiProvDomInfo",
  "suppFeat" : "suppFeat"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api-provider-management/v1/registrations',
            method='POST',
            headers=headers,
            data=json.dumps(api_provider_enrolment_details),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_registrations_registration_id_delete(self):
        """Test case for registrations_registration_id_delete

        
        """
        headers = { 
            'Accept': 'application/problem+json',
        }
        response = self.client.open(
            '/api-provider-management/v1/registrations/{registration_id}'.format(registration_id='registration_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_registrations_registration_id_put(self):
        """Test case for registrations_registration_id_put

        
        """
        api_provider_enrolment_details = {
  "regSec" : "regSec",
  "apiProvFuncs" : [ {
    "apiProvFuncId" : "apiProvFuncId",
    "apiProvFuncInfo" : "apiProvFuncInfo",
    "regInfo" : {
      "apiProvCert" : "apiProvCert",
      "apiProvPubKey" : "apiProvPubKey"
    }
  }, {
    "apiProvFuncId" : "apiProvFuncId",
    "apiProvFuncInfo" : "apiProvFuncInfo",
    "regInfo" : {
      "apiProvCert" : "apiProvCert",
      "apiProvPubKey" : "apiProvPubKey"
    }
  } ],
  "failReason" : "failReason",
  "apiProvDomId" : "apiProvDomId",
  "apiProvDomInfo" : "apiProvDomInfo",
  "suppFeat" : "suppFeat"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api-provider-management/v1/registrations/{registration_id}'.format(registration_id='registration_id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(api_provider_enrolment_details),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
