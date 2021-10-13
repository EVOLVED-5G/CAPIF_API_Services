# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from logs.models.interface_description import InterfaceDescription  # noqa: E501
from logs.models.invocation_log import InvocationLog  # noqa: E501
from logs.models.operation import Operation  # noqa: E501
from logs.models.problem_details import ProblemDetails  # noqa: E501
from logs.models.protocol import Protocol  # noqa: E501
from logs.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_api_invocation_logs_get(self):
        """Test case for api_invocation_logs_get

        
        """
        query_string = [('aef-id', 'aef_id_example'),
                        ('api-invoker-id', 'api_invoker_id_example'),
                        ('time-range-start', '2013-10-20T19:20:30+01:00'),
                        ('time-range-end', '2013-10-20T19:20:30+01:00'),
                        ('api-id', 'api_id_example'),
                        ('api-name', 'api_name_example'),
                        ('api-version', 'api_version_example'),
                        ('protocol', logs.Protocol()),
                        ('operation', logs.Operation()),
                        ('result', 'result_example'),
                        ('resource-name', 'resource_name_example'),
                        ('src-interface', logs.InterfaceDescription()),
                        ('dest-interface', logs.InterfaceDescription()),
                        ('supported-features', 'supported_features_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/logs/v1/apiInvocationLogs',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
