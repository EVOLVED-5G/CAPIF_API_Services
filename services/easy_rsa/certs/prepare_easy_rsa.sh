FILE=/root/certs/pki/ca.crt
FILE_RSA=/root/certs/EasyRSA-3.0.4
FILE_SERVER_CERTS=/root/certs/server_certs


if [ ! -f "$FILE_RSA" ]; then
    apt-get update
    apt-get upgrade -y
    apt-get install -y --no-install-recommends  wget openssl


    wget --no-check-certificate -P /root/certs/ https://github.com/OpenVPN/easy-rsa/releases/download/v3.0.4/EasyRSA-3.0.4.tgz

    tar xvf /root/certs/EasyRSA-3.0.4.tgz 
    rm /root/certs/EasyRSA-3.0.4.tgz
    cp -r /root/vars /root/certs/EasyRSA-3.0.4/vars

    echo 'PATH="EasyRSA-3.0.4/:$PATH"' >> .profile

else
    echo 'PATH="EasyRSA-3.0.4/:$PATH"' >> .profile
fi

if [ ! -f "$FILE" ]; then
    yes | /root/certs/EasyRSA-3.0.4/easyrsa init-pki
    yes | /root/certs/EasyRSA-3.0.4/easyrsa build-ca nopass
fi


mkdir $FILE_SERVER_CERTS
openssl genrsa -out $FILE_SERVER_CERTS/server.key 2048
COUNTRY="ES"                # 2 letter country-code
STATE="Madrid"            # state or province name
LOCALITY="Madrid"        # Locality Name (e.g. city)
ORGNAME="Telefonica I+D" # Organization Name (eg, company)
ORGUNIT="Innovation"                  # Organizational Unit Name (eg. section)
COMMONNAME="easy-rsa"
EMAIL="inno@tid.es"    # certificate's email address
# optional extra details
CHALLENGE=""                # challenge password
COMPANY=""                  # company name

# DAYS="-days 365"

# create the certificate request
cat <<__EOF__ | openssl req -new $DAYS -key $FILE_SERVER_CERTS/server.key -out $FILE_SERVER_CERTS/server.csr
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

openssl x509 -req -in $FILE_SERVER_CERTS/server.csr -CA $FILE -CAkey ./pki/private/ca.key  -CAcreateserial -out $FILE_SERVER_CERTS/server.crt -days 365 -sha256


python3 /root/app.py