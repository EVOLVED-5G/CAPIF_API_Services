# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from service_apis.models.communication_type import CommunicationType  # noqa: E501
from service_apis.models.data_format import DataFormat  # noqa: E501
from service_apis.models.discovered_apis import DiscoveredAPIs  # noqa: E501
from service_apis.models.problem_details import ProblemDetails  # noqa: E501
from service_apis.models.protocol import Protocol  # noqa: E501
from service_apis.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_all_service_apis_get(self):
        """Test case for all_service_apis_get

        
        """
        query_string = [('api-invoker-id', 'api_invoker_id_example'),
                        ('api-name', 'api_name_example'),
                        ('api-version', 'api_version_example'),
                        ('comm-type', service_apis.CommunicationType()),
                        ('protocol', service_apis.Protocol()),
                        ('aef-id', 'aef_id_example'),
                        ('data-format', service_apis.DataFormat()),
                        ('api-cat', 'api_cat_example'),
                        ('supported-features', 'supported_features_example'),
                        ('api-supported-features', 'api_supported_features_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/service-apis/v1/allServiceAPIs',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
