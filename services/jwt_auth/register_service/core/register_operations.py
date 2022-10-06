from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token
from ..db.db import MongoDatabse
import secrets
import requests
import json

from OpenSSL.SSL import FILETYPE_PEM
from OpenSSL.crypto import (dump_certificate_request, dump_privatekey, load_publickey, PKey, TYPE_RSA, X509Req, dump_publickey)



class RegisterOperations:

    def __init__(self):
        self.db = MongoDatabse()
        self.mimetype = 'application/json'

    def register_invoker(self, username, password, description, cn, role):

        mycol = self.db.get_col_by_name(self.db.capif_users)
        exist_user = mycol.find_one({"username": username})
        if exist_user:
            return jsonify("Invoker already exists"), 409

        user_info = dict(_id=secrets.token_hex(7), username=username, password=password, role=role, description=description, cn=cn)
        obj = mycol.insert_one(user_info)

        return jsonify(message="invoker registered successfully",
                    id=obj.inserted_id,
                    ccf_onboarding_url="api-invoker-management/v1/onboardedInvokers",
                    ccf_discover_url="service-apis/v1/allServiceAPIs?api-invoker-id="), 201


    def register_provider(self, username, password, description, cn, role):
        mycol = self.db.get_col_by_name(self.db.capif_users)
        exist_user = mycol.find_one({"username": username})
        if exist_user:
            return jsonify("Provider already exists"), 409

        user_info = dict(_id=secrets.token_hex(7), username=username, password=password, role=role, description=description, cn=cn)
        obj = mycol.insert_one(user_info)

        return jsonify(message="provider" + " registered successfully",
                    id=obj.inserted_id,
                    ccf_api_onboarding_url="api-provider-management/v1/registrations",
                    ccf_publish_url="published-apis/v1/{}/service-apis".format(obj.inserted_id)), 201

    def get_auth(self, username, password):

        mycol = self.db.get_col_by_name(self.db.capif_users)
        exist_user = mycol.find_one({"username": username, "password": password})

        if exist_user is None:
            return jsonify("Not exister user with this credentials"), 400

        if exist_user["role"] == "invoker":

            access_token = create_access_token(identity=(username + " " + exist_user["role"]))
            url = "http://easy-rsa:8080/ca-root"
            headers = {

                    'Content-Type': self.mimetype
            }
            response = requests.request("GET", url, headers=headers)
            response_payload = json.loads(response.text)
            return jsonify(message="Token and CA root returned successfully", access_token=access_token, ca_root=response_payload["certificate"]), 201

        elif exist_user == "provider":
            access_token = create_access_token(identity=(username + " " + exist_user["role"]))
            return jsonify(message="Token returned successfully", access_token=access_token), 201
