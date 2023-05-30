from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token
from ..db.db import MongoDatabse
import secrets
import requests
import json
import sys

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
                    ccf_publish_url="published-apis/v1/<apfId>/service-apis"), 201

    def get_auth(self, username, password):

        mycol = self.db.get_col_by_name(self.db.capif_users)

        try:

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

    def delete_tests(self):
        user = self.db.get_col_by_name("user")
        invokerdetails = self.db.get_col_by_name('invokerdetails')
        serviceapidescriptions = self.db.get_col_by_name('serviceapidescriptions')
        eventsdetails = self.db.get_col_by_name('eventsdetails')
        servicesecurity = self.db.get_col_by_name('security')
        providerenrolmentdetails = self.db.get_col_by_name('providerenrolmentdetails')

        splitter_string = '//'
        message_returned = ''

        myquery = {"username": {"$regex": "^ROBOT_TESTING.*"}}
        result = user.delete_many(myquery)
        if result.deleted_count == 0:
            message_returned += "No test users present"
        else:
            message_returned += "Deleted " + str(result.deleted_count) + " Test Users"
        message_returned += splitter_string

        myquery = {"description": {"$regex": "^ROBOT_TESTING.*"}}
        result = serviceapidescriptions.delete_many(myquery)
        if result.deleted_count == 0:
            message_returned += "No test services present"
        else:
            message_returned += "Deleted " + str(result.deleted_count) + " Test Services"
        message_returned += splitter_string

        myquery = {"api_invoker_information": {"$regex": "^ROBOT_TESTING.*"}}
        result = invokerdetails.delete_many(myquery)
        if result.deleted_count == 0:
            message_returned += "No test Invokers present"
        else:
            message_returned += "Deleted " + str(result.deleted_count) + " Test Invokers"
        message_returned += splitter_string

        myquery = {"notification_destination": {"$regex": "^http://robot.testing.*"}}
        result = eventsdetails.delete_many(myquery)
        if result.deleted_count == 0:
            message_returned += "No event subscription present"
        else:
            message_returned += "Deleted " + str(result.deleted_count) + " Event Subscriptions"
        message_returned += splitter_string

        myquery = {"notification_destination": {"$regex": "^http://robot.testing.*"}}
        result = servicesecurity.delete_many(myquery)
        if result.deleted_count == 0:
            message_returned += "No service security subscription present"
        else:
            message_returned += "Deleted " + str(result.deleted_count) + " service security Subscriptions"
        message_returned += splitter_string

        myquery = {"api_prov_dom_info": {"$regex": "^ROBOT_TESTING.*"}}
        result = providerenrolmentdetails.delete_many(myquery)
        if result.deleted_count == 0:
            message_returned += "No Provider Enrolment Details present"
        else:
            message_returned += "Deleted " + str(result.deleted_count) + " provider enrolment details"
        message_returned += splitter_string

        return jsonify(message=message_returned), 200


