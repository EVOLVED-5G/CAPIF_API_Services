# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from aef_security.models.check_authentication_req import CheckAuthenticationReq  # noqa: E501
from aef_security.models.check_authentication_rsp import CheckAuthenticationRsp  # noqa: E501
from aef_security.models.problem_details import ProblemDetails  # noqa: E501
from aef_security.models.revoke_authorization_req import RevokeAuthorizationReq  # noqa: E501
from aef_security.models.revoke_authorization_rsp import RevokeAuthorizationRsp  # noqa: E501
from aef_security.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_check_authentication_post(self):
        """Test case for check_authentication_post

        Check authentication.
        """
        check_authentication_req = {
  "supportedFeatures" : "supportedFeatures",
  "apiInvokerId" : "apiInvokerId"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/aef-security/v1/check-authentication',
            method='POST',
            headers=headers,
            data=json.dumps(check_authentication_req),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_revoke_authorization_post(self):
        """Test case for revoke_authorization_post

        Revoke authorization.
        """
        revoke_authorization_req = {
  "supportedFeatures" : "supportedFeatures",
  "revokeInfo" : {
    "apiInvokerId" : "apiInvokerId",
    "aefId" : "aefId",
    "apiIds" : [ "apiIds", "apiIds" ]
  }
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/aef-security/v1/revoke-authorization',
            method='POST',
            headers=headers,
            data=json.dumps(revoke_authorization_req),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
