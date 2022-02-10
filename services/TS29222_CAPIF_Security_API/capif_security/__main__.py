#!/usr/bin/env python3

import connexion

from capif_security import encoder
from flask_jwt_extended import JWTManager


app = connexion.App(__name__, specification_dir='./openapi/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'CAPIF_Security_API'},
            pythonic_params=True)

app.app.config['MONGODB_SETTINGS'] = {
    'user': 'root',
    'password': 'example',
    'db': 'capif',
    'col': 'servicesecurity',
    'invokers': 'invokerdetails',
    'jwt': 'user',
    'host': 'mongo',
    'port': 27017,
}

app.app.config["JWT_SECRET_KEY"] = "this-is-secret-key"


jwt = JWTManager(app.app)


if __name__ == '__main__':
    app.run(debug=True, port=8080)