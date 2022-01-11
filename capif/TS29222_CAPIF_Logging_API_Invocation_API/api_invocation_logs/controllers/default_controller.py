import connexion
import six

from api_invocation_logs.models.invocation_log import InvocationLog  # noqa: E501
from api_invocation_logs.models.problem_details import ProblemDetails  # noqa: E501
from api_invocation_logs import util


def aef_id_logs_post(aef_id, invocation_log):  # noqa: E501
    """aef_id_logs_post

    Creates a new log entry for service API invocations. # noqa: E501

    :param aef_id: Identifier of the API exposing function
    :type aef_id: str
    :param invocation_log: 
    :type invocation_log: dict | bytes

    :rtype: InvocationLog
    """
    if connexion.request.is_json:
        invocation_log = InvocationLog.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
