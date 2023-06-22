#!/usr/bin/env python3

from flask import Blueprint, jsonify
from ..core.operations import Operations
from flask import request
from functools import wraps
from cryptography import x509
from cryptography.hazmat.backends import default_backend


backoffice_routes = Blueprint("backoffice_routes", __name__)
operations = Operations()

def cert_validation():
    def _cert_validation(f):
        @wraps(f)
        def __cert_validation(**kwargs):

            cert_tmp = request.headers['X-Ssl-Client-Cert']
            cert_raw = cert_tmp.replace('\t', '')

            cert = x509.load_pem_x509_certificate(str.encode(cert_raw), default_backend())

            cn = cert.subject.get_attributes_for_oid(x509.OID_COMMON_NAME)[0].value.strip()

            if cn != "superadmin":
                return jsonify(message="Invalid user"), 401

            result = f(**kwargs)
            return result
        return __cert_validation
    return _cert_validation


@backoffice_routes.route("/invokers", methods=["GET"])
@cert_validation
def get_invokers():
    return operations.get_invokers()


@backoffice_routes.route("/providers", methods=["GET"])
@cert_validation
def get_providers():
    return operations.get_providers()


@backoffice_routes.route("/resources/invokers/security/<invoker_id>", methods=["GET"])
@cert_validation
def get_invoker_security_context(invoker_id):
    if invoker_id == "null":
        return jsonify(message="Invalid invoker_id", security_contexts=None), 400
    return operations.get_invoker_security_context(invoker_id)


@backoffice_routes.route("/events/<id>", methods=["GET"])
@cert_validation
def get_events(id):
    if id == "null":
        return jsonify(message="Invalid events id", object=None), 400
    return operations.get_events(id)


@backoffice_routes.route("/resources/providers/services/<id>", methods=["GET"])
@cert_validation
def get_provider_services(id):
    if id == "null":
        return jsonify(message="Invalid apf_id", object=None), 400
    return operations.get_provider_services(id)
