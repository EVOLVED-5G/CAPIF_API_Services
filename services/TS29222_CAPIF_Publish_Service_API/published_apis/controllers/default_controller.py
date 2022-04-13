import connexion
from published_apis.models.service_api_description import ServiceAPIDescription  # noqa: E501
from ..core import serviceapidescriptions

import json
from flask import Response, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import pymongo


def apf_id_service_apis_get(apf_id):  # noqa: E501
    """apf_id_service_apis_get

    Retrieve all published APIs. # noqa: E501

    :param apf_id: 
    :type apf_id: str

    :rtype: ServiceAPIDescription
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

    capif_user = capif_users.find_one({"$and": [{"cn": cn}, {"role": "apf"}]})
    if capif_user is None:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="User not authorized",
                              cause="Certificate not authorized")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    # service_apis = serviceapidescriptions.get_serviceapis(apf_id)
    # response = service_apis, 200

    res = serviceapidescriptions.get_serviceapis(apf_id)

    return res


def apf_id_service_apis_post(apf_id, body):  # noqa: E501
    """apf_id_service_apis_post

    Publish a new API. # noqa: E501

    :param apf_id: 
    :type apf_id: str
    :param service_api_description: 
    :type service_api_description: dict | bytes

    :rtype: ServiceAPIDescription
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

    capif_user = capif_users.find_one({"$and": [{"cn": cn}, {"role": "apf"}]})
    if capif_user is None:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="User not authorized", cause="Certificate not authorized")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = ServiceAPIDescription.from_dict(connexion.request.get_json())  # noqa: E501

    res = serviceapidescriptions.add_serviceapidescription(apf_id, body)
    return res


def apf_id_service_apis_service_api_id_delete(service_api_id, apf_id):  # noqa: E501
    """apf_id_service_apis_service_api_id_delete

    Unpublish a published service API. # noqa: E501

    :param service_api_id: 
    :type service_api_id: str
    :param apf_id: 
    :type apf_id: str

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

    capif_user = capif_users.find_one({"$and": [{"cn": cn}, {"role": "apf"}]})
    if capif_user is None:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="User not authorized",
                              cause="Certificate not authorized")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = ServiceAPIDescription.from_dict(connexion.request.get_json())  # noqa: E501

    # service_apis = serviceapidescriptions.delete_serviceapidescription(service_api_id, apf_id)
    # response = service_apis, 204

    res = serviceapidescriptions.delete_serviceapidescription(service_api_id, apf_id)

    return res


def apf_id_service_apis_service_api_id_get(service_api_id, apf_id):  # noqa: E501
    """apf_id_service_apis_service_api_id_get

    Retrieve a published service API. # noqa: E501

    :param service_api_id: 
    :type service_api_id: str
    :param apf_id: 
    :type apf_id: str

    :rtype: ServiceAPIDescription
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

    capif_user = capif_users.find_one({"$and": [{"cn": cn}, {"role": "apf"}]})
    if capif_user is None:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="User not authorized",
                              cause="Certificate not authorized")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    # service_apis = serviceapidescriptions.get_one_serviceapi(service_api_id, apf_id)
    # response = service_apis, 200

    res = serviceapidescriptions.get_one_serviceapi(service_api_id, apf_id)

    return res


def apf_id_service_apis_service_api_id_put(service_api_id, apf_id, body):  # noqa: E501
    """apf_id_service_apis_service_api_id_put

    Update a published service API. # noqa: E501

    :param service_api_id: 
    :type service_api_id: str
    :param apf_id: 
    :type apf_id: str
    :param service_api_description: 
    :type service_api_description: dict | bytes

    :rtype: ServiceAPIDescription
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

    capif_user = capif_users.find_one({"$and": [{"cn": cn}, {"role": "apf"}]})
    if capif_user is None:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="User not authorized",
                              cause="Certificate not authorized")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    if connexion.request.is_json:
        body = ServiceAPIDescription.from_dict(connexion.request.get_json())  # noqa: E501

    response = serviceapidescriptions.update_serviceapidescription(service_api_id, apf_id, body)
    # return response,200
    return response
