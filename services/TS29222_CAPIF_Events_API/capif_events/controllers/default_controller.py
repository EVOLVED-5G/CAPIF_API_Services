import connexion
from capif_events.models.event_subscription import EventSubscription  # noqa: E501
from ..core import eventsapis
import json
from flask import Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails


@jwt_required()
def subscriber_id_subscriptions_post(subscriber_id, body):  # noqa: E501
    """subscriber_id_subscriptions_post

    Creates a new individual CAPIF Event Subscription. # noqa: E501

    :param subscriber_id: Identifier of the Subscriber
    :type subscriber_id: str
    :param event_subscription: 
    :type event_subscription: dict | bytes

    :rtype: EventSubscription
    """
    identity = get_jwt_identity()
    _, role = identity.split()


    ## Put here any role (apf or invoker)
    if role != "apf" and role !="invoker":
        prob = ProblemDetails(title="Unauthorized", status=401, detail="Role not authorized for this API route",
                                cause="User role must be apf")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = EventSubscription.from_dict(connexion.request.get_json())  # noqa: E501

    

    res = eventsapis.post_event(subscriber_id, body)

    return res



@jwt_required()
def subscriber_id_subscriptions_subscription_id_delete(subscriber_id, subscription_id):  # noqa: E501
    """subscriber_id_subscriptions_subscription_id_delete

    Deletes an individual CAPIF Event Subscription. # noqa: E501

    :param subscriber_id: Identifier of the Subscriber
    :type subscriber_id: str
    :param subscription_id: Identifier of an individual Events Subscription
    :type subscription_id: str

    :rtype: None
    """

    identity = get_jwt_identity()
    _, role = identity.split()


    ## Put here any role (apf or invoker)
    if role != "apf" and role !="invoker":
        prob = ProblemDetails(title="Unauthorized", status=401, detail="Role not authorized for this API route",
                                cause="User role must be apf")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = EventSubscription.from_dict(connexion.request.get_json())  # noqa: E501


    res = eventsapis.delete_event(subscriber_id, subscription_id)

    return res
