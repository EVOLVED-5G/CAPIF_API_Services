# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api_invocation_logs.models.base_model_ import Model
from api_invocation_logs.models.operation_any_of import OperationAnyOf
from api_invocation_logs import util

from api_invocation_logs.models.operation_any_of import OperationAnyOf  # noqa: E501

class Operation(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self):  # noqa: E501
        """Operation - a model defined in OpenAPI

        """
        self.openapi_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'Operation':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Operation of this Operation.  # noqa: E501
        :rtype: Operation
        """
        return util.deserialize_model(dikt, cls)
