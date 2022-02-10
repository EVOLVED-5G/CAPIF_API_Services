import connexion
import six

from capif_events.models.event_subscription import EventSubscription  # noqa: E501
from capif_events.models.problem_details import ProblemDetails  # noqa: E501
from capif_events import util


def subscriber_id_subscriptions_post(subscriber_id, event_subscription):  # noqa: E501
    """subscriber_id_subscriptions_post

    Creates a new individual CAPIF Event Subscription. # noqa: E501

    :param subscriber_id: Identifier of the Subscriber
    :type subscriber_id: str
    :param event_subscription: 
    :type event_subscription: dict | bytes

    :rtype: EventSubscription
    """
    if connexion.request.is_json:
        event_subscription = EventSubscription.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def subscriber_id_subscriptions_subscription_id_delete(subscriber_id, subscription_id):  # noqa: E501
    """subscriber_id_subscriptions_subscription_id_delete

    Deletes an individual CAPIF Event Subscription. # noqa: E501

    :param subscriber_id: Identifier of the Subscriber
    :type subscriber_id: str
    :param subscription_id: Identifier of an individual Events Subscription
    :type subscription_id: str

    :rtype: None
    """
    return 'do some magic!'
