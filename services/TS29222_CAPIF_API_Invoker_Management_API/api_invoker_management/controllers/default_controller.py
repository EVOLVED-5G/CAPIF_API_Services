import connexion

from api_invoker_management.models.api_invoker_enrolment_details import APIInvokerEnrolmentDetails  # noqa: E501
from ..core.apiinvokerenrolmentdetails import InvokerManagementOperations
from ..core.validate_user import ControlAccess

import json
from flask import Response, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from ..core.publisher import Publisher
from functools import wraps
import pymongo

invoker_operations = InvokerManagementOperations()
publisher_ops = Publisher()
valid_user = ControlAccess()


def cert_validation():
    def _cert_validation(f):
        @wraps(f)
        def __cert_validation(*args, **kwargs):
            #just do here everything what you need

            args = request.view_args
            cert_tmp = request.headers['X-Ssl-Client-Cert']
            cert_raw = cert_tmp.replace('\t', '')

            cert = x509.load_pem_x509_certificate(str.encode(cert_raw), default_backend())

            cn = cert.subject.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value.strip()

            if cn != "superadmin":
                cert_signature = cert.signature.hex()
                result = valid_user.validate_user_cert(args["onboardingId"], cert_signature)

                if result is not None:
                    return result

            result = f(**kwargs)
            return result
        return __cert_validation
    return _cert_validation

@cert_validation()
def onboarded_invokers_onboarding_id_delete(onboarding_id):  # noqa: E501
    """onboarded_invokers_onboarding_id_delete

    Deletes an individual API Invoker. # noqa: E501

    :param onboarding_id: String identifying an individual on-boarded API invoker resource
    :type onboarding_id: str

    :rtype: None
    """

    current_app.logger.info("Removing invoker")
    res = invoker_operations.remove_apiinvokerenrolmentdetail(onboarding_id)

    if res.status_code == 204:
        current_app.logger.info("Invoker Removed")
        publisher_ops.publish_message("events", "API_INVOKER_UPDATED")
        publisher_ops.publish_message("internal-messages", f"invoker-removed:{onboarding_id}")

    return res

@cert_validation()
def onboarded_invokers_onboarding_id_put(onboarding_id, body):  # noqa: E501
    """onboarded_invokers_onboarding_id_put

    Updates an individual API invoker details. # noqa: E501

    :param onboarding_id: String identifying an individual on-boarded API invoker resource
    :type onboarding_id: str
    :param api_invoker_enrolment_details: representation of the API invoker details to be updated in CAPIF core function
    :type api_invoker_enrolment_details: dict | bytes

    :rtype: APIInvokerEnrolmentDetails
    """
    current_app.logger.info("Updating invoker")
    if connexion.request.is_json:
        body = APIInvokerEnrolmentDetails.from_dict(connexion.request.get_json())  # noqa: E501
    res = invoker_operations.update_apiinvokerenrolmentdetail(onboarding_id,body)

    if res.status_code == 200:
        current_app.logger.info("Invoker Updated")
        publisher_ops.publish_message("events", "API_INVOKER_UPDATED")

    return res


@jwt_required()
def onboarded_invokers_post(body):  # noqa: E501
    """onboarded_invokers_post

    Creates a new individual API Invoker profile. # noqa: E501

    :param api_invoker_enrolment_details:
    :type api_invoker_enrolment_details: dict | bytes

    :rtype: APIInvokerEnrolmentDetails
    """

    identity = get_jwt_identity()
    _, role = identity.split()

    if role != "invoker":
        prob = ProblemDetails(title="Unauthorized", status=401, detail="Role not authorized for this API route",
                              cause="User role must be invoker")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = APIInvokerEnrolmentDetails.from_dict(connexion.request.get_json())  # noqa: E501

    current_app.logger.info("Creating Invoker")
    res = invoker_operations.add_apiinvokerenrolmentdetail(body)
    if res.status_code == 201:
        current_app.logger.info("Invoker Created")
        publisher_ops.publish_message("events", "API_INVOKER_ONBOARDED")

    return res
