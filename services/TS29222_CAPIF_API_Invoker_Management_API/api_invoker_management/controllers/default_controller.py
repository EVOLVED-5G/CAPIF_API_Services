import connexion

from api_invoker_management.models.api_invoker_enrolment_details import APIInvokerEnrolmentDetails  # noqa: E501
from ..core import apiinvokerenrolmentdetails

import json
from flask import Response, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import pymongo


def onboarded_invokers_onboarding_id_delete(onboarding_id):  # noqa: E501
    """onboarded_invokers_onboarding_id_delete

    Deletes an individual API Invoker. # noqa: E501

    :param onboarding_id: String identifying an individual on-boarded API invoker resource
    :type onboarding_id: str

    :rtype: None
    """
    cert_tmp = request.headers['X-Ssl-Client-Cert']
    cert_raw = cert_tmp.replace('\t', '')
    # print(cert_raw)
    # sys.stdout.flush()

    cert = x509.load_pem_x509_certificate(str.encode(cert_raw), default_backend())
    cn = cert.subject.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value.strip()
    # print(cn)
    # sys.stdout.flush()

    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    cap_users = current_app.config['MONGODB_SETTINGS']['jwt']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    capif_users = mydb[cap_users]

    capif_user = capif_users.find_one({"$and": [{"cn": cn}, {"role": "invoker"}]})

    if capif_user is None:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="User not authorized",
                              cause="Certificate not authorized")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    return apiinvokerenrolmentdetails.remove_apiinvokerenrolmentdetail(onboarding_id)


def onboarded_invokers_onboarding_id_put(onboarding_id, body):  # noqa: E501
    """onboarded_invokers_onboarding_id_put

    Updates an individual API invoker details. # noqa: E501

    :param onboarding_id: String identifying an individual on-boarded API invoker resource
    :type onboarding_id: str
    :param api_invoker_enrolment_details: representation of the API invoker details to be updated in CAPIF core function
    :type api_invoker_enrolment_details: dict | bytes

    :rtype: APIInvokerEnrolmentDetails
    """
    cert_tmp = request.headers['X-Ssl-Client-Cert']
    cert_raw = cert_tmp.replace('\t', '')
    # print(cert_raw)
    # sys.stdout.flush()

    cert = x509.load_pem_x509_certificate(str.encode(cert_raw), default_backend())
    cn = cert.subject.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value.strip()
    # print(cn)
    # sys.stdout.flush()

    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    cap_users = current_app.config['MONGODB_SETTINGS']['jwt']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    capif_users = mydb[cap_users]

    capif_user = capif_users.find_one({"$and": [{"cn": cn}, {"role": "invoker"}]})

    if capif_user is None:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="User not authorized",
                              cause="Certificate not authorized")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = APIInvokerEnrolmentDetails.from_dict(connexion.request.get_json())  # noqa: E501
    res = apiinvokerenrolmentdetails.update_apiinvokerenrolmentdetail(onboarding_id,body)
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
    username, role = identity.split()

    if role != "invoker":
        prob = ProblemDetails(title="Unauthorized", status=401, detail="Role not authorized for this API route",
                              cause="User role must be invoker")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = APIInvokerEnrolmentDetails.from_dict(connexion.request.get_json())  # noqa: E501

    res = apiinvokerenrolmentdetails.add_apiinvokerenrolmentdetail(body)
    return res
