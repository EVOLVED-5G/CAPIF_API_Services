import connexion
import six

from api_invoker_management.models.api_invoker_enrolment_details import APIInvokerEnrolmentDetails  # noqa: E501
from api_invoker_management.models.problem_details import ProblemDetails  # noqa: E501
from api_invoker_management import util
from ..core import apiinvokerenrolmentdetails

import pymongo
import secrets
import json
from flask_jwt_extended import jwt_required


def onboarded_invokers_onboarding_id_delete(onboarding_id):  # noqa: E501
    """onboarded_invokers_onboarding_id_delete

    Deletes an individual API Invoker. # noqa: E501

    :param onboarding_id: String identifying an individual on-boarded API invoker resource
    :type onboarding_id: str

    :rtype: None
    """
    return 'do some magic!'


def onboarded_invokers_onboarding_id_put(onboarding_id, api_invoker_enrolment_details):  # noqa: E501
    """onboarded_invokers_onboarding_id_put

    Updates an individual API invoker details. # noqa: E501

    :param onboarding_id: String identifying an individual on-boarded API invoker resource
    :type onboarding_id: str
    :param api_invoker_enrolment_details: representation of the API invoker details to be updated in CAPIF core function
    :type api_invoker_enrolment_details: dict | bytes

    :rtype: APIInvokerEnrolmentDetails
    """
    if connexion.request.is_json:
        api_invoker_enrolment_details = APIInvokerEnrolmentDetails.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


@jwt_required()
def onboarded_invokers_post(body):  # noqa: E501
    """onboarded_invokers_post

    Creates a new individual API Invoker profile. # noqa: E501

    :param api_invoker_enrolment_details:
    :type api_invoker_enrolment_details: dict | bytes

    :rtype: APIInvokerEnrolmentDetails
    """

    if connexion.request.is_json:
        body = APIInvokerEnrolmentDetails.from_dict(connexion.request.get_json())  # noqa: E501

    res = apiinvokerenrolmentdetails.add_apiinvokerenrolmentdetail(body)
    return res
