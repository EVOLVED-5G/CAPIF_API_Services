curl --request GET 'http://easy_rsa:8080/ca-root' 2>/dev/null | jq -r '.certificate' -j > /etc/nginx/certs/ca.crt

site="capifcore"
folder="/etc/nginx/certs"
cd $folder

openssl genrsa -out client.key 2048

COUNTRY="ES"                # 2 letter country-code
STATE="Madrid"            # state or province name
LOCALITY="Madrid"        # Locality Name (e.g. city)
ORGNAME="Telefonica I+D" # Organization Name (eg, company)
ORGUNIT="Innovation"                  # Organizational Unit Name (eg. section)
EMAIL="inno@tid.es"    # certificate's email address
# optional extra details
CHALLENGE=""                # challenge password
COMPANY=""                  # company name

DAYS="-days 365"

# create the certificate request
cat <<__EOF__ | openssl req -new $DAYS -nodes -keyout client.key -out client.csr
$COUNTRY
$STATE
$LOCALITY
$ORGNAME
$ORGUNIT
$site
$EMAIL
$CHALLENGE
$COMPANY
__EOF__

awk -v cert="$(cat client.csr)" 'BEGIN{gsub(/\n/, "\\n", cert)} {sub(/"CERT"/, "\"" cert "\"")} 1' sign_req_body_tmp.json > sign_req_body.json
curl --location --request POST 'http://easy_rsa:8080/sign-csr' --header 'Content-Type: application/json' -d @./sign_req_body.json | jq -r '.certificate' -j > /etc/nginx/certs/client.crt

nginx