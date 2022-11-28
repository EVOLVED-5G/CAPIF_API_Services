#!/bin/bash
EASY_RSA_HOSTNAME="easy-rsa"
EASY_RSA_PORT="8080"
CERTS_FOLDER="/etc/nginx/certs"
cd $CERTS_FOLDER

curl  --retry 30 \
    --retry-all-errors \
    --connect-timeout 5 \
    --max-time 10 \
    --retry-delay 10 \
    --retry-max-time 300 \
    --request GET "http://$EASY_RSA_HOSTNAME:$EASY_RSA_PORT/ca-root" 2>/dev/null | jq -r '.certificate' -j > $CERTS_FOLDER/ca.crt

openssl verify -CAfile $CERTS_FOLDER/ca.crt $CERTS_FOLDER/ca.crt
rc=$?
if [ $rc -eq 0 ]
then
    echo "CA root Certificate downloaded successfull"
else
    echo "Failure: CA root certificate is not valid"
    exit $rc
fi

openssl genrsa -out $CERTS_FOLDER/server.key 2048

echo "NGINX Hostname is $CAPIF_HOSTNAME"

COUNTRY="ES"                # 2 letter country-code
STATE="Madrid"            # state or province name
LOCALITY="Madrid"        # Locality Name (e.g. city)
ORGNAME="Telefonica I+D" # Organization Name (eg, company)
ORGUNIT="Innovation"                  # Organizational Unit Name (eg. section)
COMMONNAME="$CAPIF_HOSTNAME"
EMAIL="inno@tid.es"    # certificate's email address
# optional extra details
CHALLENGE=""                # challenge password
COMPANY=""                  # company name

# DAYS="-days 365"

# create the certificate request
#cat <<__EOF__ | openssl req -new $DAYS -nodes -keyout client.key -out client.csr
cat <<__EOF__ | openssl req -new $DAYS -key $CERTS_FOLDER/server.key -out $CERTS_FOLDER/server.csr
$COUNTRY
$STATE
$LOCALITY
$ORGNAME
$ORGUNIT
$COMMONNAME
$EMAIL
$CHALLENGE
$COMPANY
__EOF__

awk -v cert="$(cat $CERTS_FOLDER/server.csr)" 'BEGIN{gsub(/\n/, "\\n", cert)} {sub(/"CERT"/, "\"" cert "\"")} 1' $CERTS_FOLDER/sign_req_body_tmp.json > $CERTS_FOLDER/sign_req_body.json
curl  --retry 30 \
    --retry-all-errors \
    --connect-timeout 5 \
    --max-time 10 \
    --retry-delay 10 \
    --retry-max-time 300 \
    --location --request POST "http://$EASY_RSA_HOSTNAME:$EASY_RSA_PORT/sign-csr" --header 'Content-Type: application/json' -d @./sign_req_body.json | jq -r '.certificate' -j > $CERTS_FOLDER/server.crt


redis-cli -h redis -p 6379 -n 1 -x SET server_priv_key < $CERTS_FOLDER/server.key
openssl x509 -pubkey -noout -in $CERTS_FOLDER/server.crt  > $CERTS_FOLDER/pubkey.pem
redis-cli -h redis -p 6379 -n 1 -x SET server_pub_key < $CERTS_FOLDER/pubkey.pem

nginx