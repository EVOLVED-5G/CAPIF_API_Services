# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from capif_events.models.base_model_ import Model
from capif_events.models.time_range_list import TimeRangeList
from capif_events import util

from capif_events.models.time_range_list import TimeRangeList  # noqa: E501

class ApiInvokerPolicy(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, api_invoker_id=None, allowed_total_invocations=None, allowed_invocations_per_second=None, allowed_invocation_time_range_list=None):  # noqa: E501
        """ApiInvokerPolicy - a model defined in OpenAPI

        :param api_invoker_id: The api_invoker_id of this ApiInvokerPolicy.  # noqa: E501
        :type api_invoker_id: str
        :param allowed_total_invocations: The allowed_total_invocations of this ApiInvokerPolicy.  # noqa: E501
        :type allowed_total_invocations: int
        :param allowed_invocations_per_second: The allowed_invocations_per_second of this ApiInvokerPolicy.  # noqa: E501
        :type allowed_invocations_per_second: int
        :param allowed_invocation_time_range_list: The allowed_invocation_time_range_list of this ApiInvokerPolicy.  # noqa: E501
        :type allowed_invocation_time_range_list: List[TimeRangeList]
        """
        self.openapi_types = {
            'api_invoker_id': str,
            'allowed_total_invocations': int,
            'allowed_invocations_per_second': int,
            'allowed_invocation_time_range_list': List[TimeRangeList]
        }

        self.attribute_map = {
            'api_invoker_id': 'apiInvokerId',
            'allowed_total_invocations': 'allowedTotalInvocations',
            'allowed_invocations_per_second': 'allowedInvocationsPerSecond',
            'allowed_invocation_time_range_list': 'allowedInvocationTimeRangeList'
        }

        self._api_invoker_id = api_invoker_id
        self._allowed_total_invocations = allowed_total_invocations
        self._allowed_invocations_per_second = allowed_invocations_per_second
        self._allowed_invocation_time_range_list = allowed_invocation_time_range_list

    @classmethod
    def from_dict(cls, dikt) -> 'ApiInvokerPolicy':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ApiInvokerPolicy of this ApiInvokerPolicy.  # noqa: E501
        :rtype: ApiInvokerPolicy
        """
        return util.deserialize_model(dikt, cls)

    @property
    def api_invoker_id(self):
        """Gets the api_invoker_id of this ApiInvokerPolicy.

        API invoker ID assigned by the CAPIF core function  # noqa: E501

        :return: The api_invoker_id of this ApiInvokerPolicy.
        :rtype: str
        """
        return self._api_invoker_id

    @api_invoker_id.setter
    def api_invoker_id(self, api_invoker_id):
        """Sets the api_invoker_id of this ApiInvokerPolicy.

        API invoker ID assigned by the CAPIF core function  # noqa: E501

        :param api_invoker_id: The api_invoker_id of this ApiInvokerPolicy.
        :type api_invoker_id: str
        """
        if api_invoker_id is None:
            raise ValueError("Invalid value for `api_invoker_id`, must not be `None`")  # noqa: E501

        self._api_invoker_id = api_invoker_id

    @property
    def allowed_total_invocations(self):
        """Gets the allowed_total_invocations of this ApiInvokerPolicy.

        Total number of invocations allowed on the service API by the API invoker.  # noqa: E501

        :return: The allowed_total_invocations of this ApiInvokerPolicy.
        :rtype: int
        """
        return self._allowed_total_invocations

    @allowed_total_invocations.setter
    def allowed_total_invocations(self, allowed_total_invocations):
        """Sets the allowed_total_invocations of this ApiInvokerPolicy.

        Total number of invocations allowed on the service API by the API invoker.  # noqa: E501

        :param allowed_total_invocations: The allowed_total_invocations of this ApiInvokerPolicy.
        :type allowed_total_invocations: int
        """

        self._allowed_total_invocations = allowed_total_invocations

    @property
    def allowed_invocations_per_second(self):
        """Gets the allowed_invocations_per_second of this ApiInvokerPolicy.

        Invocations per second allowed on the service API by the API invoker.  # noqa: E501

        :return: The allowed_invocations_per_second of this ApiInvokerPolicy.
        :rtype: int
        """
        return self._allowed_invocations_per_second

    @allowed_invocations_per_second.setter
    def allowed_invocations_per_second(self, allowed_invocations_per_second):
        """Sets the allowed_invocations_per_second of this ApiInvokerPolicy.

        Invocations per second allowed on the service API by the API invoker.  # noqa: E501

        :param allowed_invocations_per_second: The allowed_invocations_per_second of this ApiInvokerPolicy.
        :type allowed_invocations_per_second: int
        """

        self._allowed_invocations_per_second = allowed_invocations_per_second

    @property
    def allowed_invocation_time_range_list(self):
        """Gets the allowed_invocation_time_range_list of this ApiInvokerPolicy.

        The time ranges during which the invocations are allowed on the service API by the API invoker.  # noqa: E501

        :return: The allowed_invocation_time_range_list of this ApiInvokerPolicy.
        :rtype: List[TimeRangeList]
        """
        return self._allowed_invocation_time_range_list

    @allowed_invocation_time_range_list.setter
    def allowed_invocation_time_range_list(self, allowed_invocation_time_range_list):
        """Sets the allowed_invocation_time_range_list of this ApiInvokerPolicy.

        The time ranges during which the invocations are allowed on the service API by the API invoker.  # noqa: E501

        :param allowed_invocation_time_range_list: The allowed_invocation_time_range_list of this ApiInvokerPolicy.
        :type allowed_invocation_time_range_list: List[TimeRangeList]
        """
        if allowed_invocation_time_range_list is not None and len(allowed_invocation_time_range_list) < 0:
            raise ValueError("Invalid value for `allowed_invocation_time_range_list`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._allowed_invocation_time_range_list = allowed_invocation_time_range_list
