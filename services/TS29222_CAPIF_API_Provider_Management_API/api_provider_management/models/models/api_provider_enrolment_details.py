# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api_provider_management.models.base_model_ import Model
from api_provider_management.models.api_provider_function_details import APIProviderFunctionDetails
import re
from api_provider_management import util

from api_provider_management.models.api_provider_function_details import APIProviderFunctionDetails  # noqa: E501
import re  # noqa: E501

class APIProviderEnrolmentDetails(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, api_prov_dom_id=None, reg_sec=None, api_prov_funcs=None, api_prov_dom_info=None, supp_feat=None, fail_reason=None):  # noqa: E501
        """APIProviderEnrolmentDetails - a model defined in OpenAPI

        :param api_prov_dom_id: The api_prov_dom_id of this APIProviderEnrolmentDetails.  # noqa: E501
        :type api_prov_dom_id: str
        :param reg_sec: The reg_sec of this APIProviderEnrolmentDetails.  # noqa: E501
        :type reg_sec: str
        :param api_prov_funcs: The api_prov_funcs of this APIProviderEnrolmentDetails.  # noqa: E501
        :type api_prov_funcs: List[APIProviderFunctionDetails]
        :param api_prov_dom_info: The api_prov_dom_info of this APIProviderEnrolmentDetails.  # noqa: E501
        :type api_prov_dom_info: str
        :param supp_feat: The supp_feat of this APIProviderEnrolmentDetails.  # noqa: E501
        :type supp_feat: str
        :param fail_reason: The fail_reason of this APIProviderEnrolmentDetails.  # noqa: E501
        :type fail_reason: str
        """
        self.openapi_types = {
            'api_prov_dom_id': str,
            'reg_sec': str,
            'api_prov_funcs': List[APIProviderFunctionDetails],
            'api_prov_dom_info': str,
            'supp_feat': str,
            'fail_reason': str
        }

        self.attribute_map = {
            'api_prov_dom_id': 'apiProvDomId',
            'reg_sec': 'regSec',
            'api_prov_funcs': 'apiProvFuncs',
            'api_prov_dom_info': 'apiProvDomInfo',
            'supp_feat': 'suppFeat',
            'fail_reason': 'failReason'
        }

        self._api_prov_dom_id = api_prov_dom_id
        self._reg_sec = reg_sec
        self._api_prov_funcs = api_prov_funcs
        self._api_prov_dom_info = api_prov_dom_info
        self._supp_feat = supp_feat
        self._fail_reason = fail_reason

    @classmethod
    def from_dict(cls, dikt) -> 'APIProviderEnrolmentDetails':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The APIProviderEnrolmentDetails of this APIProviderEnrolmentDetails.  # noqa: E501
        :rtype: APIProviderEnrolmentDetails
        """
        return util.deserialize_model(dikt, cls)

    @property
    def api_prov_dom_id(self):
        """Gets the api_prov_dom_id of this APIProviderEnrolmentDetails.

        API provider domain ID assigned by the CAPIF core function to the API management function while registering the API provider domain. Shall not be present in the HTTP POST request from the API Management function to the CAPIF core function, to on-board itself. Shall be present in all other HTTP requests and responses.   # noqa: E501

        :return: The api_prov_dom_id of this APIProviderEnrolmentDetails.
        :rtype: str
        """
        return self._api_prov_dom_id

    @api_prov_dom_id.setter
    def api_prov_dom_id(self, api_prov_dom_id):
        """Sets the api_prov_dom_id of this APIProviderEnrolmentDetails.

        API provider domain ID assigned by the CAPIF core function to the API management function while registering the API provider domain. Shall not be present in the HTTP POST request from the API Management function to the CAPIF core function, to on-board itself. Shall be present in all other HTTP requests and responses.   # noqa: E501

        :param api_prov_dom_id: The api_prov_dom_id of this APIProviderEnrolmentDetails.
        :type api_prov_dom_id: str
        """

        self._api_prov_dom_id = api_prov_dom_id

    @property
    def reg_sec(self):
        """Gets the reg_sec of this APIProviderEnrolmentDetails.

        Security information necessary for the CAPIF core function to validate the registration of the API provider domain. Shall be present in HTTP POST request from API management function to CAPIF core function for API provider domain registration.   # noqa: E501

        :return: The reg_sec of this APIProviderEnrolmentDetails.
        :rtype: str
        """
        return self._reg_sec

    @reg_sec.setter
    def reg_sec(self, reg_sec):
        """Sets the reg_sec of this APIProviderEnrolmentDetails.

        Security information necessary for the CAPIF core function to validate the registration of the API provider domain. Shall be present in HTTP POST request from API management function to CAPIF core function for API provider domain registration.   # noqa: E501

        :param reg_sec: The reg_sec of this APIProviderEnrolmentDetails.
        :type reg_sec: str
        """
        if reg_sec is None:
            raise ValueError("Invalid value for `reg_sec`, must not be `None`")  # noqa: E501

        self._reg_sec = reg_sec

    @property
    def api_prov_funcs(self):
        """Gets the api_prov_funcs of this APIProviderEnrolmentDetails.

        A list of individual API provider domain functions details. When included by the API management function in the HTTP request message, it lists the API provider domain functions that the API management function intends to register/update in registration or update registration procedure. When included by the CAPIF core function in the HTTP response message, it lists the API domain functions details that are registered or updated successfully.   # noqa: E501

        :return: The api_prov_funcs of this APIProviderEnrolmentDetails.
        :rtype: List[APIProviderFunctionDetails]
        """
        return self._api_prov_funcs

    @api_prov_funcs.setter
    def api_prov_funcs(self, api_prov_funcs):
        """Sets the api_prov_funcs of this APIProviderEnrolmentDetails.

        A list of individual API provider domain functions details. When included by the API management function in the HTTP request message, it lists the API provider domain functions that the API management function intends to register/update in registration or update registration procedure. When included by the CAPIF core function in the HTTP response message, it lists the API domain functions details that are registered or updated successfully.   # noqa: E501

        :param api_prov_funcs: The api_prov_funcs of this APIProviderEnrolmentDetails.
        :type api_prov_funcs: List[APIProviderFunctionDetails]
        """
        if api_prov_funcs is not None and len(api_prov_funcs) < 1:
            raise ValueError("Invalid value for `api_prov_funcs`, number of items must be greater than or equal to `1`")  # noqa: E501

        self._api_prov_funcs = api_prov_funcs

    @property
    def api_prov_dom_info(self):
        """Gets the api_prov_dom_info of this APIProviderEnrolmentDetails.

        Generic information related to the API provider domain such as details of the API provider applications.   # noqa: E501

        :return: The api_prov_dom_info of this APIProviderEnrolmentDetails.
        :rtype: str
        """
        return self._api_prov_dom_info

    @api_prov_dom_info.setter
    def api_prov_dom_info(self, api_prov_dom_info):
        """Sets the api_prov_dom_info of this APIProviderEnrolmentDetails.

        Generic information related to the API provider domain such as details of the API provider applications.   # noqa: E501

        :param api_prov_dom_info: The api_prov_dom_info of this APIProviderEnrolmentDetails.
        :type api_prov_dom_info: str
        """

        self._api_prov_dom_info = api_prov_dom_info

    @property
    def supp_feat(self):
        """Gets the supp_feat of this APIProviderEnrolmentDetails.

        A string used to indicate the features supported by an API that is used as defined in clause  6.6 in 3GPP TS 29.500. The string shall contain a bitmask indicating supported features in  hexadecimal representation Each character in the string shall take a value of \"0\" to \"9\",  \"a\" to \"f\" or \"A\" to \"F\" and shall represent the support of 4 features as described in  table 5.2.2-3. The most significant character representing the highest-numbered features shall  appear first in the string, and the character representing features 1 to 4 shall appear last  in the string. The list of features and their numbering (starting with 1) are defined  separately for each API. If the string contains a lower number of characters than there are  defined features for an API, all features that would be represented by characters that are not  present in the string are not supported.   # noqa: E501

        :return: The supp_feat of this APIProviderEnrolmentDetails.
        :rtype: str
        """
        return self._supp_feat

    @supp_feat.setter
    def supp_feat(self, supp_feat):
        """Sets the supp_feat of this APIProviderEnrolmentDetails.

        A string used to indicate the features supported by an API that is used as defined in clause  6.6 in 3GPP TS 29.500. The string shall contain a bitmask indicating supported features in  hexadecimal representation Each character in the string shall take a value of \"0\" to \"9\",  \"a\" to \"f\" or \"A\" to \"F\" and shall represent the support of 4 features as described in  table 5.2.2-3. The most significant character representing the highest-numbered features shall  appear first in the string, and the character representing features 1 to 4 shall appear last  in the string. The list of features and their numbering (starting with 1) are defined  separately for each API. If the string contains a lower number of characters than there are  defined features for an API, all features that would be represented by characters that are not  present in the string are not supported.   # noqa: E501

        :param supp_feat: The supp_feat of this APIProviderEnrolmentDetails.
        :type supp_feat: str
        """
        if supp_feat is not None and not re.search(r'^[A-Fa-f0-9]*$', supp_feat):  # noqa: E501
            raise ValueError("Invalid value for `supp_feat`, must be a follow pattern or equal to `/^[A-Fa-f0-9]*$/`")  # noqa: E501

        self._supp_feat = supp_feat

    @property
    def fail_reason(self):
        """Gets the fail_reason of this APIProviderEnrolmentDetails.

        Registration or update specific failure information of failed API provider domain function registrations.Shall be present in the HTTP response body if atleast one of the API provider domain function registration or update registration fails.   # noqa: E501

        :return: The fail_reason of this APIProviderEnrolmentDetails.
        :rtype: str
        """
        return self._fail_reason

    @fail_reason.setter
    def fail_reason(self, fail_reason):
        """Sets the fail_reason of this APIProviderEnrolmentDetails.

        Registration or update specific failure information of failed API provider domain function registrations.Shall be present in the HTTP response body if atleast one of the API provider domain function registration or update registration fails.   # noqa: E501

        :param fail_reason: The fail_reason of this APIProviderEnrolmentDetails.
        :type fail_reason: str
        """

        self._fail_reason = fail_reason
