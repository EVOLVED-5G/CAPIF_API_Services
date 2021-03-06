# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api_invoker_management.models.base_model_ import Model
from api_invoker_management import util


class ShareableInformation(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, is_shareable=None, capif_prov_doms=None):  # noqa: E501
        """ShareableInformation - a model defined in OpenAPI

        :param is_shareable: The is_shareable of this ShareableInformation.  # noqa: E501
        :type is_shareable: bool
        :param capif_prov_doms: The capif_prov_doms of this ShareableInformation.  # noqa: E501
        :type capif_prov_doms: List[str]
        """
        self.openapi_types = {
            'is_shareable': bool,
            'capif_prov_doms': List[str]
        }

        self.attribute_map = {
            'is_shareable': 'isShareable',
            'capif_prov_doms': 'capifProvDoms'
        }

        self._is_shareable = is_shareable
        self._capif_prov_doms = capif_prov_doms

    @classmethod
    def from_dict(cls, dikt) -> 'ShareableInformation':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ShareableInformation of this ShareableInformation.  # noqa: E501
        :rtype: ShareableInformation
        """
        return util.deserialize_model(dikt, cls)

    @property
    def is_shareable(self):
        """Gets the is_shareable of this ShareableInformation.

        Set to \"true\" indicates that the service API and/or the service API category can be shared to the list of CAPIF provider domain information. Otherwise set to \"false\".  # noqa: E501

        :return: The is_shareable of this ShareableInformation.
        :rtype: bool
        """
        return self._is_shareable

    @is_shareable.setter
    def is_shareable(self, is_shareable):
        """Sets the is_shareable of this ShareableInformation.

        Set to \"true\" indicates that the service API and/or the service API category can be shared to the list of CAPIF provider domain information. Otherwise set to \"false\".  # noqa: E501

        :param is_shareable: The is_shareable of this ShareableInformation.
        :type is_shareable: bool
        """
        if is_shareable is None:
            raise ValueError("Invalid value for `is_shareable`, must not be `None`")  # noqa: E501

        self._is_shareable = is_shareable

    @property
    def capif_prov_doms(self):
        """Gets the capif_prov_doms of this ShareableInformation.

        List of CAPIF provider domains to which the service API information to be shared.  # noqa: E501

        :return: The capif_prov_doms of this ShareableInformation.
        :rtype: List[str]
        """
        return self._capif_prov_doms

    @capif_prov_doms.setter
    def capif_prov_doms(self, capif_prov_doms):
        """Sets the capif_prov_doms of this ShareableInformation.

        List of CAPIF provider domains to which the service API information to be shared.  # noqa: E501

        :param capif_prov_doms: The capif_prov_doms of this ShareableInformation.
        :type capif_prov_doms: List[str]
        """
        if capif_prov_doms is not None and len(capif_prov_doms) < 1:
            raise ValueError("Invalid value for `capif_prov_doms`, number of items must be greater than or equal to `1`")  # noqa: E501

        self._capif_prov_doms = capif_prov_doms
