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


    def register_aef(self, username, password, description, cn, role):
        mycol = self.db.get_col_by_name(self.db.capif_users)
        exist_user = mycol.find_one({"username": username})
        if exist_user:
            return jsonify("Exposer already exists"), 409

        user_info = dict(_id=secrets.token_hex(7), username=username, password=password, role=role, description=description, cn=cn)
        obj = mycol.insert_one(user_info)

        return jsonify(message="exposer" + " registered successfully",
                    id=obj.inserted_id,
                    ccf_publish_url="published-apis/v1/{}/service-apis".format(obj.inserted_id)), 201

    def get_auth(self, username, password, role):

        if role == "invoker":
            mycol = self.db.get_col_by_name(self.db.capif_users)
            exist_user = mycol.find_one({"username": username, "password": password, "role": role})
            if exist_user:
                access_token = create_access_token(identity=(username + " " + role))
                url = "http://easy-rsa:8080/ca-root"
                headers = {

                        'Content-Type': self.mimetype
                }
                response = requests.request("GET", url, headers=headers)
                response_payload = json.loads(response.text)
                return jsonify(message="Token and CA root returned successfully", access_token=access_token, ca_root=response_payload["certificate"]), 201
            else:
                return jsonify(message="Bad credentials. User not found"), 401
        elif role == "exposer":
            mycol = self.db.get_col_by_name(self.db.capif_users)
            exist_user = mycol.find_one({"username": username, "password": password, "role": role})

            if exist_user:
                try:
                    csr_request, private_key = self.create_csr()
                    publick_key = csr_request.decode("utf-8")
                    url = "http://easy-rsa:8080/sign-csr"

                    payload = dict()
                    payload['csr'] = publick_key
                    payload['mode'] = 'client'
                    payload['filename'] = username

                    headers = {

                        'Content-Type': self.mimetype

                    }

                    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
                    response_payload = json.loads(response.text)

                    return jsonify(message="Certificate created successfuly", cert=response_payload["certificate"], private_key=private_key.decode("utf-8")), 201

                except Exception as e:
                    return jsonify(message="Error while create certificate: "+ str(e)), 500
            else:
                return jsonify(message="Bad credentials. User not found"), 401


    def create_csr(self):

        # create public/private key
        key = PKey()
        key.generate_key(TYPE_RSA, 2048)

        # Generate CSR
        req = X509Req()
        req.get_subject().CN = 'Exposer'
        req.get_subject().O = 'Telefonica I+D'
        req.get_subject().C = 'ES'
        req.set_pubkey(key)
        req.sign(key, 'sha256')


        csr_request = dump_certificate_request(FILETYPE_PEM, req)

        private_key = dump_privatekey(FILETYPE_PEM, key)

        return csr_request, private_key