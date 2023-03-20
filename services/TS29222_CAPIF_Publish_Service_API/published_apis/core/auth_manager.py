
from flask import current_app
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from .resources import Resource


class AuthManager(Resource):

    def add_auth_service(self, service_id, apf_id):
        cert_col = self.db.get_col_by_name(self.db.certs_col)

        auth_context = cert_col.find_one({"id":apf_id})

        if "services" in auth_context["resources"]:
            if service_id not in auth_context["resources"]["services"]:
                auth_context["resources"]["services"].append(service_id)
        else:
            auth_context["resources"]["services"] = [service_id]

        current_app.logger.info(auth_context)
        cert_col.find_one_and_update({"id":apf_id}, {"$set":auth_context})


    def remove_auth_service(self, service_id, apf_id):

        cert_col = self.db.get_col_by_name(self.db.certs_col)

        auth_context = cert_col.find_one({"id":apf_id})

        if "services" in auth_context["resources"]:
            if service_id in auth_context["resources"]["services"]:
                auth_context["resources"]["services"].remove(service_id)

        cert_col.find_one_and_update({"id":apf_id}, {"$set":auth_context})

    def remove_auth_all_service(self, apf_id):

        cert_col = self.db.get_col_by_name(self.db.certs_col)

        auth_context = cert_col.find_one({"id":apf_id})

        if "services" in auth_context["resources"]:
            auth_context["resources"]["services"] = []

        cert_col.find_one_and_update({"id":apf_id}, {"$set":auth_context})
