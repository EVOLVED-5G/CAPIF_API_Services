import requests
import json
import configparser
import redis
import os

# Get environment variables
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

from OpenSSL.SSL import FILETYPE_PEM
from OpenSSL.crypto import (dump_certificate_request, dump_privatekey, load_publickey, PKey, TYPE_RSA, X509Req, dump_publickey)


def create_csr(csr_file_path):
    private_key_path = "private.key"

    # create public/private key
    key = PKey()
    key.generate_key(TYPE_RSA, 2048)

    # Generate CSR
    req = X509Req()
    req.get_subject().CN = 'dummy'
    req.get_subject().O = 'Telefonica I+D'
    req.get_subject().OU = 'Innovation'
    req.get_subject().L = 'Madrid'
    req.get_subject().ST = 'Madrid'
    req.get_subject().C = 'ES'
    req.get_subject().emailAddress = 'inno@tid.es'
    req.set_pubkey(key)
    req.sign(key, 'sha256')

    with open(csr_file_path, 'wb+') as f:
        f.write(dump_certificate_request(FILETYPE_PEM, req))
        csr_request = dump_certificate_request(FILETYPE_PEM, req)
    with open(private_key_path, 'wb+') as f:
        f.write(dump_privatekey(FILETYPE_PEM, key))

    return csr_request


def register_netapp_to_capif(capif_ip, capif_port, username, password, role, description, cn):
    url = "http://{}:{}/register".format(capif_ip, capif_port)

    payload = dict()
    payload['username'] = username
    payload['password'] = password
    payload['role'] = role
    payload['description'] = description
    payload['cn'] = cn

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_payload = json.loads(response.text)
        return response_payload['id'], response_payload['ccf_onboarding_url'], response_payload['ccf_discover_url'],
    except requests.exceptions.HTTPError as err:
        raise Exception(err.response.text, err.response.status_code)


def get_capif_token(capif_ip, capif_port, username, password, role):
    url = "http://{}:{}/gettoken".format(capif_ip, capif_port)

    payload = dict()
    payload['username'] = username
    payload['password'] = password
    payload['role'] = role

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_payload = json.loads(response.text)
        return response_payload['access_token']
    except requests.exceptions.HTTPError as err:
        raise Exception(err.response.text, err.response.status_code)


def onboard_netapp_to_capif(capif_ip, capif_callback_ip, capif_callback_port, jwt_token, ccf_url):
    url = 'https://{}/{}'.format(capif_ip, ccf_url)

    csr_request = create_csr("cert_req.csr")

    json_file = open('invoker_details.json', 'rb')
    payload_dict = json.load(json_file)
    payload_dict['onboardingInformation']['apiInvokerPublicKey'] = csr_request.decode("utf-8")
    payload_dict['notificationDestination'] = payload_dict['notificationDestination'].replace("X", capif_callback_ip)
    payload_dict['notificationDestination'] = payload_dict['notificationDestination'].replace("Y", capif_callback_port)
    payload = json.dumps(payload_dict)

    headers = {
        'Authorization': 'Bearer {}'.format(jwt_token),
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
        response_payload = json.loads(response.text)
        certification_file = open('dummy.crt', 'wb')
        certification_file.write(bytes(response_payload['onboardingInformation']['apiInvokerCertificate'], 'utf-8'))
        certification_file.close()
        return response_payload['apiInvokerId']
    except requests.exceptions.HTTPError as err:
        raise Exception(err.response.text, err.response.status_code)


def discover_service_apis(capif_ip, api_invoker_id, jwt_token, ccf_url):
    url = "https://{}/{}{}".format(capif_ip, ccf_url, api_invoker_id)

    payload = {}
    files = {}
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload, files=files, cert=('dummy.crt', 'private.key'), verify='ca.crt')
        response.raise_for_status()
        response_payload = json.loads(response.text)
        return response_payload
    except requests.exceptions.HTTPError as err:
        print(err.response.text)
        message = json.loads(err.response.text)
        status = err.response.status_code
        raise Exception(message, status)


# if __name__ == '__main__':

#     r = redis.Redis(
#         host=REDIS_HOST,
#         port=REDIS_PORT,
#         decode_responses=True,
#     )

#     config = configparser.ConfigParser()
#     config.read('credentials.properties')

#     username = config.get("credentials", "invoker_username")
#     password = config.get("credentials", "invoker_password")
#     role = config.get("credentials", "invoker_role")
#     description = config.get("credentials", "invoker_description")
#     cn = config.get("credentials", "invoker_cn")
#     capif_ip = config.get("credentials", "capif_ip")
#     capif_port = config.get("credentials", "capif_port")
#     capif_callback_ip = config.get("credentials", "capif_callback_ip")
#     capif_callback_port = config.get("credentials", "capif_callback_port")

#     try:
#         if not r.exists('netappID'):
#             netappID, ccf_onboarding_url, ccf_discover_url = register_netapp_to_capif(capif_ip, capif_port, username, password, role, description, cn)
#             r.set('netappID', netappID)
#             r.set('ccf_onboarding_url', ccf_onboarding_url)
#             r.set('ccf_discover_url', ccf_discover_url)
#             print("NetAppID: {}\n".format(netappID))
#     except Exception as e:
#         status_code = e.args[1]
#         if status_code == 409:
#             print("User already registed. Continue with token request\n")
#         else:
#             print(e)

#     try:
#         if not r.exists('capif_access_token'):
#             capif_access_token = get_capif_token(capif_ip, capif_port, username, password, role)
#             r.set('capif_access_token', capif_access_token)
#             print("Capif Token: {}\n".format(capif_access_token))
#     except Exception as e:
#         status_code = e.args[1]
#         if status_code == 401:
#             print("Bad credentials. User not found\n")
#         else:
#             print(e)
#         capif_access_token = None

#     try:
#         if not r.exists('invokerID'):
#             capif_access_token = r.get('capif_access_token')
#             ccf_onboarding_url = r.get('ccf_onboarding_url')
#             invokerID = onboard_netapp_to_capif(capif_ip, capif_callback_ip, capif_callback_port, capif_access_token, ccf_onboarding_url)
#             r.set('invokerID', invokerID)
#             print("ApiInvokerID: {}\n".format(invokerID))
#     except Exception as e:
#         status_code = e.args[1]
#         if status_code == 401:
#             capif_access_token = get_capif_token(capif_ip, capif_port, username, password, role)
#             r.set('capif_access_token', capif_access_token)
#             ccf_onboarding_url = r.get('ccf_onboarding_url')
#             print("New Capif Token: {}\n".format(capif_access_token))
#             invokerID = onboard_netapp_to_capif(capif_ip, capif_callback_ip, capif_callback_port, capif_access_token, ccf_onboarding_url)
#             r.set('invokerID', invokerID)
#             print("ApiInvokerID: {}\n".format(invokerID))
#         elif status_code == 403:
#             print("Invoker already registered.")
#             print("Chanage invoker public key in invoker_details.json\n")
#         else:
#             print(e)

#     try:
#         if r.exists('invokerID'):
#             invokerID = r.get('invokerID')
#             capif_access_token = r.get('capif_access_token')
#             ccf_discover_url = r.get('ccf_discover_url')
#             discovered_apis = discover_service_apis(capif_ip, invokerID, capif_access_token, ccf_discover_url)
#             print("Discovered APIs")
#             print(json.dumps(discovered_apis, indent=2))
#     except Exception as e:
#         status_code = e.args[1]
#         if status_code == 401:
#             print("API Invoker is not authorized")
#         elif status_code == 403:
#             print("API Invoker does not exist. API Invoker id not found")
#         else:
#             print(e)