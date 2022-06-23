curl --request GET 'http://easy_rsa:8080/ca-root' 2>/dev/null | jq -r '.certificate' -j > /etc/nginx/certs/ca.crt

folder="/etc/nginx/certs"
cd $folder

openssl genrsa -out server.key 2048

COUNTRY="ES"                # 2 letter country-code
STATE="Madrid"            # state or province name
LOCALITY="Madrid"        # Locality Name (e.g. city)
ORGNAME="Telefonica I+D" # Organization Name (eg, company)
ORGUNIT="Innovation"                  # Organizational Unit Name (eg. section)
COMMONNAME="$CN"
EMAIL="inno@tid.es"    # certificate's email address
# optional extra details
CHALLENGE=""                # challenge password
COMPANY=""                  # company name

DAYS="-days 365"

# create the certificate request
#cat <<__EOF__ | openssl req -new $DAYS -nodes -keyout client.key -out client.csr
cat <<__EOF__ | openssl req -new $DAYS -key server.key -out server.csr
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

awk -v cert="$(cat server.csr)" 'BEGIN{gsub(/\n/, "\\n", cert)} {sub(/"CERT"/, "\"" cert "\"")} 1' sign_req_body_tmp.json > sign_req_body.json
curl --location --request POST 'http://easy_rsa:8080/sign-csr' --header 'Content-Type: application/json' -d @./sign_req_body.json | jq -r '.certificate' -j > /etc/nginx/certs/server.crt

nginx