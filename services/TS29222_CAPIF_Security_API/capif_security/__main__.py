#!/usr/bin/env python3

import connexion

from capif_security import encoder
from flask_jwt_extended import JWTManager
import sys


def main():

    with open("/usr/src/app/capif_security/server.key", "rb") as key_file:
            key_data = key_file.read()

    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder

    jwt = JWTManager(app.app)
    app.app.config['JWT_ALGORITHM'] = 'RS256'
    app.app.config['JWT_PRIVATE_KEY'] = key_data
    app.add_api('openapi.yaml',
                arguments={'title': 'CAPIF_Security_API'},
                pythonic_params=True)

    app.run(port=8080, debug=True)

if __name__ == '__main__':
    main()

