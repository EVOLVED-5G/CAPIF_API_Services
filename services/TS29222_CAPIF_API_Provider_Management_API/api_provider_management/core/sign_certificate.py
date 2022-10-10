import requests
import json
import sys

def sign_certificate(publick_key, information):
    url = "http://easy-rsa:8080/sign-csr"

    payload = dict()
    payload['csr'] = publick_key
    payload['mode'] = 'client'
    payload['filename'] = information

    headers = {

        'Content-Type': "application/json"

    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    response_payload = json.loads(response.text)

    return response_payload["certificate"]