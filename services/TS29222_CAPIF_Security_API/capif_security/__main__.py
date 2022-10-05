#!/usr/bin/env python3

import connexion

from capif_security import encoder
from flask_jwt_extended import JWTManager
import sys


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'CAPIF_Security_API'},
                pythonic_params=True)

    app.run(port=8080, debug=True)

if __name__ == '__main__':
    main()

