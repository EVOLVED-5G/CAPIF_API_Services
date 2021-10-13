# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from access_control_policy.models.access_control_policy_list import AccessControlPolicyList  # noqa: E501
from access_control_policy.models.problem_details import ProblemDetails  # noqa: E501
from access_control_policy.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_access_control_policy_list_service_api_id_get(self):
        """Test case for access_control_policy_list_service_api_id_get

        
        """
        query_string = [('aef-id', 'aef_id_example'),
                        ('api-invoker-id', 'api_invoker_id_example'),
                        ('supported-features', 'supported_features_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/access-control-policy/v1/accessControlPolicyList/{service_api_id}'.format(service_api_id='service_api_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
