import requests
import json


def send_ca_to_capif():
    url = "http://jwtauth:8080/ca"

    capif_ca = open('/home/adminca/pki/ca.crt', 'rb')
    capif_ca_crt = capif_ca.read()
    capif_ca.close()

    payload = dict()
    payload['certificate'] = capif_ca_crt.decode("utf-8")

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        return response
    except requests.exceptions.HTTPError as err:
        raise Exception(err.response.text, err.response.status_code)


if __name__ == '__main__':
    send_ca_to_capif()