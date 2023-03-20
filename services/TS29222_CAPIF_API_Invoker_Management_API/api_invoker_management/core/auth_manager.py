
from flask import current_app
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from .resources import Resource


class AuthManager(Resource):

    def add_auth_invoker(self, cert, invoker_id):
        cert_col = self.db.get_col_by_name(self.db.certs_col)

        cert_encode = x509.load_pem_x509_certificate(str.encode(cert), default_backend())
        cert_col.insert_one({"cert_signature":cert_encode.signature.hex(), "role":"invoker", "id": invoker_id, "resources": {}})

    def update_auth_invoker(self, cert, invoker_id):
        cert_col = self.db.get_col_by_name(self.db.certs_col)

        cert_encode = x509.load_pem_x509_certificate(str.encode(cert), default_backend())
        cert_col.find_one_and_update({"id":invoker_id}, {"$set":{"cert_signature":cert_encode.signature.hex()}})

    def remove_auth_invoker(self, invoker_id):
        cert_col = self.db.get_col_by_name(self.db.certs_col)

        cert_col.delete_one({"id":invoker_id})
