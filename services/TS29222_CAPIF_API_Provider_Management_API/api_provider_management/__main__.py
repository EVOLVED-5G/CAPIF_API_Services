#!/usr/bin/env python3

import connexion

from api_provider_management import encoder
from flask_jwt_extended import JWTManager


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'CAPIF_API_Provider_Management_API'},
                pythonic_params=True)

    app.app.config["JWT_SECRET_KEY"] = "this-is-secret-key"
    JWTManager(app.app)


    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
