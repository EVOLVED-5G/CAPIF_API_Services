#!/usr/bin/env python3

import connexion

from api_invoker_management import encoder


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'CAPIF_API_Invoker_Management_API'},
                pythonic_params=True)
    app.app.config['MONGODB_SETTINGS'] = {
        'user': 'root',
        'password': 'example',
        'db': 'capif',
        'col': 'invokerdetails',
        'host': 'mongo',
        'port': 27017,
    }

    app.run(port=8080)


if __name__ == '__main__':
    main()
