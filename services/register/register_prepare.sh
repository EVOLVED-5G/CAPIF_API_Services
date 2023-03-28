#!/bin/bash

# sleep 10
# redis-cli -h redis -p 6379 -n 1 GET  server_priv_key > /usr/src/app/register_service/server.key

destdir=/usr/src/app/register_service/server.key
pwd=$(pwd)
echo "$CAPIF_PRIV_KEY" > "$destdir"

openssl req -x509 \
            -sha256 -days 356 \
            -nodes \
            -newkey rsa:2048 \
            -subj "/CN=register/C=ES/L=Madrid" \
            -keyout $pwd/register_service/registerCA.key -out $pwd/register_service/registerCA.crt

openssl genrsa -out $pwd/register_service/register_key.key 2048

COUNTRY="ES"                # 2 letter country-code
STATE="Madrid"            # state or province name
LOCALITY="Madrid"        # Locality Name (e.g. city)
ORGNAME="Telefonica I+D" # Organization Name (eg, company)
ORGUNIT="Innovation"                  # Organizational Unit Name (eg. section)
COMMONNAME="register"
EMAIL="inno@tid.es"    # certificate's email address
# optional extra details
CHALLENGE=""                # challenge password
COMPANY=""                  # company name

# DAYS="-days 365"

# create the certificate request
cat <<__EOF__ | openssl req -new $DAYS -key $pwd/register_service/register_key.key -out $pwd/register_service/register.csr
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

openssl x509 -req -in $pwd/register_service/register.csr -CA $pwd/register_service/registerCA.crt -CAkey $pwd/register_service/registerCA.key  -CAcreateserial -out $pwd/register_service/register_cert.crt -days 365 -sha256

cd /usr/src/app/
python3 -m register_service