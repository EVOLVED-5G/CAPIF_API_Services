#!/bin/bash

# OUTPUT=$(redis-cli -h redis -p 6379 -n 1 GET  server_priv_key)
# echo "$OUTPUT"

# if [ -z "$OUTPUT" ]; then
#     echo "OUTPUT empty"
#     exit 1;
# else
#     echo "OUTPUT: $OUTPUT"
#     redis-cli -h redis -p 6379 -n 1 GET  server_priv_key > /usr/src/app/backoffice_service/server.key
# fi

pwd=$(pwd)
openssl req -x509 \
            -sha256 -days 356 \
            -nodes \
            -newkey rsa:2048 \
            -subj "/CN=backoffice/C=ES/L=Madrid" \
            -keyout $pwd/backoffice_service/backofficeCA.key -out $pwd/backoffice_service/backofficeCA.crt

openssl genrsa -out $pwd/backoffice_service/backoffice_key.key 2048

COUNTRY="ES"                # 2 letter country-code
STATE="Madrid"            # state or province name
LOCALITY="Madrid"        # Locality Name (e.g. city)
ORGNAME="Telefonica I+D" # Organization Name (eg, company)
ORGUNIT="Innovation"                  # Organizational Unit Name (eg. section)
COMMONNAME="backoffice"
EMAIL="inno@tid.es"    # certificate's email address
# optional extra details
CHALLENGE=""                # challenge password
COMPANY=""                  # company name
# DAYS="-days 365"

# create the certificate request
cat <<__EOF__ | openssl req -new $DAYS -key $pwd/backoffice_service/backoffice_key.key -out $pwd/backoffice_service/backoffice.csr
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

openssl x509 -req -in $pwd/backoffice_service/backoffice.csr -CA $pwd/backoffice_service/backofficeCA.crt -CAkey $pwd/backoffice_service/backofficeCA.key  -CAcreateserial -out $pwd/backoffice_service/backoffice_cert.crt -days 365 -sha256

cd /usr/src/app/
python3 -m backoffice_service