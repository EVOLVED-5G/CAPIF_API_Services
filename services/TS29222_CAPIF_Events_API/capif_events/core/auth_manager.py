
from flask import current_app
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from .resources import Resource


class AuthManager(Resource):

    def add_auth_event(self, event_id, subscriber_id):

        try:

            cert_col = self.db.get_col_by_name(self.db.certs_col)

            auth_context = cert_col.find_one({"id":subscriber_id})

            if "event_subscriptions" in auth_context["resources"]:
                if event_id not in auth_context["resources"]["event_subscriptions"]:
                    auth_context["resources"]["event_subscriptions"].append(event_id)
            else:
                auth_context["resources"]["event_subscriptions"] = [event_id]

            cert_col.find_one_and_update({"id":subscriber_id}, {"$set":auth_context})

        except Exception as e:
            current_app.logger.error(f"Something wrong in add auth resources: {e}")


    def remove_auth_event(self, event_id, subscriber_id):

        try:

            cert_col = self.db.get_col_by_name(self.db.certs_col)

            auth_context = cert_col.find_one({"id":subscriber_id})

            if auth_context != None and cert_col != None:
                if "event_subscriptions" in auth_context["resources"]:
                    if event_id in auth_context["resources"]["event_subscriptions"]:
                        auth_context["resources"]["event_subscriptions"].remove(event_id)

                cert_col.find_one_and_update({"id":subscriber_id}, {"$set":auth_context})

        except Exception as e:
            current_app.logger.info(f"Something wrong in remove auth resources: {e}")

    def remove_auth_all_event(self, subscriber_id):

        try:
            cert_col = self.db.get_col_by_name(self.db.certs_col)

            auth_context = cert_col.find_one({"id":subscriber_id})

            if auth_context != None and cert_col != None:
                if "event_subscriptions" in auth_context["resources"]:
                    auth_context["resources"]["event_subscriptions"] = []

                cert_col.find_one_and_update({"id":subscriber_id}, {"$set":auth_context})

        except Exception as e:
            current_app.logger.error(f"Something wrong in remove all auth resources: {e}")
