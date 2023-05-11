import connexion
from capif_events.models.event_subscription import EventSubscription  # noqa: E501
from ..core.events_apis import EventSubscriptionsOperations
import json
from flask import Response, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from ..core.validate_user import ControlAccess
from functools import wraps
import pymongo

events_ops = EventSubscriptionsOperations()
valid_user = ControlAccess()

def cert_validation():
    def _cert_validation(f):
        @wraps(f)
        def __cert_validation(*args, **kwargs):

            args = request.view_args
            cert_tmp = request.headers['X-Ssl-Client-Cert']
            cert_raw = cert_tmp.replace('\t', '')

            cert = x509.load_pem_x509_certificate(str.encode(cert_raw), default_backend())

            cn = cert.subject.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value.strip()

            if cn != "superadmin":
                cert_signature = cert.signature.hex()
                result = valid_user.validate_user_cert(args["subscriptionId"], args["subscriberId"], cert_signature)

                if result is not None:
                    return result

            result = f(**kwargs)
            return result
        return __cert_validation
    return _cert_validation

def subscriber_id_subscriptions_post(subscriber_id, body):  # noqa: E501
    """subscriber_id_subscriptions_post

    Creates a new individual CAPIF Event Subscription. # noqa: E501

    :param subscriber_id: Identifier of the Subscriber
    :type subscriber_id: str
    :param event_subscription: 
    :type event_subscription: dict | bytes

    :rtype: EventSubscription
    """

    current_app.logger.info("Creating event subscription")
    if connexion.request.is_json:
        body = EventSubscription.from_dict(connexion.request.get_json())  # noqa: E501

    res = events_ops.create_event(subscriber_id, body)

    return res

@cert_validation()
def subscriber_id_subscriptions_subscription_id_delete(subscriber_id, subscription_id):  # noqa: E501
    """subscriber_id_subscriptions_subscription_id_delete

    Deletes an individual CAPIF Event Subscription. # noqa: E501

    :param subscriber_id: Identifier of the Subscriber
    :type subscriber_id: str
    :param subscription_id: Identifier of an individual Events Subscription
    :type subscription_id: str

    :rtype: None
    """

    current_app.logger.info("Removing event subscription")

    res = events_ops.delete_event(subscriber_id, subscription_id)

    return res
