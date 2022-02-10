# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from capif_routing_info.models.problem_details import ProblemDetails  # noqa: E501
from capif_routing_info.models.routing_info import RoutingInfo  # noqa: E501
from capif_routing_info.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_service_apis_service_api_id_get(self):
        """Test case for service_apis_service_api_id_get

        
        """
        query_string = [('aef-id', 'aef_id_example'),
                        ('supp-feat', 'supp_feat_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/capif-routing-info/v1/service-apis/{service_api_id}'.format(service_api_id='service_api_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
