#!/bin/bash
USER=dummy
if [ "$#" -eq 1 ]; then
    USER=$1
fi

/root/EasyRSA-3.0.4/easyrsa --batch revoke $USER
rm -rf /root/$USER.csr
rm -rf /root/pki/issued/$USER.crt
rm -rf /root/pki/reqs/$USER.req
