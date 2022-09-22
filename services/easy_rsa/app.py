#!/usr/bin/env python3

from typing import List
from flask import Flask, jsonify, request, Response, current_app
import json
import subprocess
import sys
import os
from pathlib import Path

app = Flask(__name__)


@app.route("/ca-root", methods=["GET"])
def return_ca_root():
    capif_ca = open('/root/pki/ca.crt', 'rb')
    capif_ca_crt = capif_ca.read()
    capif_ca.close()

    payload = dict()
    payload['certificate'] = capif_ca_crt.decode("utf-8")

    res = Response(json.dumps(payload), status=201,
                   mimetype='application/json')

    return res


@app.route("/sign-csr", methods=["POST"])
def sign_csr():
    csr = request.json["csr"]
    mode = request.json["mode"]
    filename = request.json["filename"]

    app.logger.info("sign-csr for user "+ filename)
    names = get_files(filename)

    if len(names) != 0:
        revoke_list(names)

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

    res = Response(json.dumps(payload), status=201,
                   mimetype='application/json')

    return res


@app.route("/certdata", methods=["DELETE"])
def data_test():
    names = get_files('ROBOT_TESTING')

    return revoke_list(names)

def get_files(prefix):
    files = []
    dir_list = os.listdir()
    for file in dir_list:
        if file.startswith(prefix):
            files.append(file)

    print(files)

    names = []
    for file in files:
        names.append(Path(file).stem)

    convert_list_to_set = set(names)
    names = list(convert_list_to_set)
    print("Entities to remove", names)
    return names

def revoke_cert(name):
    p = subprocess.call("/root/EasyRSA-3.0.4/easyrsa --batch revoke {}".format(name),
                        stdout=subprocess.PIPE, shell=True)
    delete_file('/root/{}.csr'.format(name))
    delete_file('/root/pki/issued/{}.crt'.format(name))
    delete_file('/root/pki/reqs/{}.req'.format(name))
    current_app.logger.info("cert %s removed", name)


def revoke_list(names=list):
    for name in names:
        revoke_cert(name)

    res = Response(json.dumps({'certificate_removed': names}),
                   status=200, mimetype='application/json')
    return res


def delete_file(filePath):
    # As file at filePath is deleted now, so we should check if file exists or not not before deleting them
    if os.path.exists(filePath):
        os.remove(filePath)
    else:
        print("Can not delete the file as it doesn't exists")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
