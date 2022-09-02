# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api_provider_management.models.api_provider_enrolment_details import APIProviderEnrolmentDetails  # noqa: E501
from api_provider_management.models.api_provider_enrolment_details_patch import APIProviderEnrolmentDetailsPatch  # noqa: E501
from api_provider_management.models.problem_details import ProblemDetails  # noqa: E501
from api_provider_management.test import BaseTestCase


class TestIndividualAPIProviderEnrolmentDetailsController(BaseTestCase):
    """IndividualAPIProviderEnrolmentDetailsController integration test stubs"""

    def test_modify_ind_api_provider_enrolment(self):
        """Test case for modify_ind_api_provider_enrolment

        
        """
        api_provider_enrolment_details_patch = api_provider_management.APIProviderEnrolmentDetailsPatch()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/merge-patch+json',
        }
        response = self.client.open(
            '/api-provider-management/v1/registrations/{registration_id}'.format(registration_id='registration_id_example'),
            method='PATCH',
            headers=headers,
            data=json.dumps(api_provider_enrolment_details_patch),
            content_type='application/merge-patch+json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
