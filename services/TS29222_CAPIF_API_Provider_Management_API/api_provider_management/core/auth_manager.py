
from flask import current_app
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from .resources import Resource


class AuthManager(Resource):

    def add_auth_provider(self, cert, func_id, role, provider_id):
        cert_col = self.db.get_col_by_name(self.db.certs_col)

        cert_encode = x509.load_pem_x509_certificate(str.encode(cert), default_backend())

        cert_col.insert_one({"cert_signature":cert_encode.signature.hex(), "provider_id": provider_id, "role":role,"id": func_id, "resources": {}})

    def update_auth_provider(self, cert, func_id, provider_id, role):
        cert_col = self.db.get_col_by_name(self.db.certs_col)

        cert_encode = x509.load_pem_x509_certificate(str.encode(cert), default_backend())
        cert_col.find_one_and_update({"provider_id":provider_id, "role":role}, {"$set":{"cert_signature":cert_encode.signature.hex(), "id":func_id}})

    def remove_auth_provider(self, func_ids):

        cert_col = self.db.get_col_by_name(self.db.certs_col)
        for func_id in func_ids:
            cert_col.delete_one({"id":func_id})
