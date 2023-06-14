#!/usr/bin/env python3

from flask import Blueprint, jsonify
from ..core.operations import Operations

backoffice_routes = Blueprint("backoffice_routes", __name__)
operations = Operations()


@backoffice_routes.route("/invokers", methods=["GET"])
def get_invokers():
    return operations.get_invokers()


@backoffice_routes.route("/providers", methods=["GET"])
def get_providers():
    return operations.get_providers()


@backoffice_routes.route("/resources/invokers/security/<invoker_id>", methods=["GET"])
def get_invoker_security_context(invoker_id):
    if invoker_id == "null":
        return jsonify(message="Invalid invoker_id", security_contexts=None), 400
    return operations.get_invoker_security_context(invoker_id)


@backoffice_routes.route("/events/<id>", methods=["GET"])
def get_events(id):
    if id == "null":
        return jsonify(message="Invalid events id", object=None), 400
    return operations.get_events(id)


@backoffice_routes.route("/resources/providers/services/<id>", methods=["GET"])
def get_provider_services(id):
    if id == "null":
        return jsonify(message="Invalid apf_id", object=None), 400
    return operations.get_provider_services(id)
