#!/bin/bash
DUMMY=dummy
CUSTOMER_EXPOSER=customexposer
./revoke_user.sh $DUMMY
./revoke_user.sh $CUSTOMER_EXPOSER

# /root/EasyRSA-3.0.4/easyrsa --batch revoke $DUMMY
# rm -rf /root/$DUMMY.csr
# rm -rf /root/pki/issued/$DUMMY.crt
# rm -rf /root/pki/reqs/$DUMMY.req

# /root/EasyRSA-3.0.4/easyrsa --batch revoke $CUSTOMER_EXPOSER
# rm -rf /root/$CUSTOMER_EXPOSER.csr
# rm -rf /root/pki/issued/$CUSTOMER_EXPOSER.crt
# rm -rf /root/pki/reqs/$CUSTOMER_EXPOSER.req
