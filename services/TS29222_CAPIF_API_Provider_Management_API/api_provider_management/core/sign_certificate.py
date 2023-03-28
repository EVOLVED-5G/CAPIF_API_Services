import requests
import json
import sys
from ..config import Config

def sign_certificate(publick_key, information):

    config =  Config().get_config()
    url = f"https://{config['ca_factory']['url']}:{config['ca_factory']['port']}/sign-csr"

    payload = dict()
    payload['csr'] = publick_key
    payload['mode'] = 'client'
    payload['filename'] = information

    headers = {

        'Content-Type': "application/json"

    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify = False)
    response_payload = json.loads(response.text)

    return response_payload["certificate"]