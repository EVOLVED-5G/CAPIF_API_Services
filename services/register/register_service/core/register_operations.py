from flask import Flask, jsonify, request, current_app
from flask_jwt_extended import create_access_token
from ..db.db import MongoDatabse
from ..config import Config
import secrets
import requests
import json
import sys

class RegisterOperations:

    def __init__(self):
        self.db = MongoDatabse()
        self.mimetype = 'application/json'
        self.config = Config().get_config()

    def register_user(self, username, password, description, cn, role):

        mycol = self.db.get_col_by_name(self.db.capif_users)
        exist_user = mycol.find_one({"username": username})
        if exist_user:
            return jsonify("user already exists"), 409

        user_info = dict(_id=secrets.token_hex(7), username=username, password=password, role=role, description=description, cn=cn)
        obj = mycol.insert_one(user_info)

        if role == "invoker":
            return jsonify(message="invoker registered successfully",
                        id=obj.inserted_id,
                        ccf_onboarding_url="api-invoker-management/v1/onboardedInvokers",
                        ccf_discover_url="service-apis/v1/allServiceAPIs?api-invoker-id="), 201
        else:
            return jsonify(message="provider" + " registered successfully",
                    id=obj.inserted_id,
                    ccf_api_onboarding_url="api-provider-management/v1/registrations",
                    ccf_publish_url="published-apis/v1/<apfId>/service-apis"), 201


    def get_auth(self, username, password):

        mycol = self.db.get_col_by_name(self.db.capif_users)

        try:

            exist_user = mycol.find_one({"username": username, "password": password})

            if exist_user is None:
                return jsonify("Not exister user with this credentials"), 400

            if exist_user["role"] == "invoker":

                access_token = create_access_token(identity=(username + " " + exist_user["role"]))
                url = f"https://{self.config['ca_factory']['url']}:{self.config['ca_factory']['port']}/ca-root"
                headers = {

                        'Content-Type': self.mimetype
                }
                response = requests.request("GET", url, headers=headers, verify = False)
                response_payload = json.loads(response.text)
                return jsonify(message="Token and CA root returned successfully", access_token=access_token, ca_root=response_payload["certificate"]), 200

            elif exist_user["role"] == "provider":
                access_token = create_access_token(identity=(username + " " + exist_user["role"]))
                return jsonify(message="Token returned successfully", access_token=access_token), 200
        except Exception as e:
            return jsonify(message=f"Errors when try getting auth: {e}"), 500

    def remove_user(self, username, password):
        mycol = self.db.get_col_by_name(self.db.capif_users)

        try:
            mycol.delete_one({"username": username, "password": password})
            return jsonify(message="User removed successfully"), 204
        except Exception as e:
            return jsonify(message=f"Errors when try remove user: {e}"), 500

