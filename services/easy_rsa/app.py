#!/usr/bin/env python3

from flask import Flask, jsonify, request, Response
import json
import subprocess
import sys
import os

app = Flask(__name__)


@app.route("/ca-root", methods=["GET"])
def return_ca_root():
    capif_ca = open('/root/pki/ca.crt', 'rb')
    capif_ca_crt = capif_ca.read()
    capif_ca.close()

    payload = dict()
    payload['certificate'] = capif_ca_crt.decode("utf-8")

    res = Response(json.dumps(payload), status=201, mimetype='application/json')

    return res


@app.route("/sign-csr", methods=["POST"])
def sign_csr():
    csr = request.json["csr"]
    mode = request.json["mode"]
    filename = request.json["filename"]

    csr_file = open(filename + '.csr', 'wb')
    csr_file.write(bytes(csr, 'utf-8'))
    csr_file.close()

    p = subprocess.call("/root/EasyRSA-3.0.4/easyrsa import-req {} {}".format(filename + '.csr', filename),
                         stdout=subprocess.PIPE, shell=True)

    p = subprocess.call("/root/EasyRSA-3.0.4/easyrsa --batch sign-req {} {}".format(mode, filename),
                         shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    cert = open('/root/pki/issued/{}.crt'.format(filename), 'rb')
    crt = cert.read()
    cert.close()

    payload = dict()
    payload['certificate'] = crt.decode("utf-8")

    res = Response(json.dumps(payload), status=201, mimetype='application/json')

    return res

@app.route("/certdata", methods=["DELETE"])
def data_test():
    filename='ROBOT_TESTING'
    p = subprocess.call("/root/EasyRSA-3.0.4/easyrsa --batch revoke {}".format(filename),
                         stdout=subprocess.PIPE, shell=True)

    delete_file('/root/ROBOT_TESTING.csr')
    delete_file('/root/pki/issued/ROBOT_TESTING.crt')
    delete_file('/root/pki/reqs/ROBOT_TESTING.req')

    res = Response(json.dumps({'certificate_removed':'ROBOT_TESTING'}), status=200, mimetype='application/json')
    return res

def delete_file(filePath):
    # As file at filePath is deleted now, so we should check if file exists or not not before deleting them
    if os.path.exists(filePath):
        os.remove(filePath)
    else:
        print("Can not delete the file as it doesn't exists")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
