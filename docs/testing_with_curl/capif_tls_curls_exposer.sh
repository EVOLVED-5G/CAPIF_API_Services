##### Execute Exposer curls locally

##### Configure machine 

##### Add in /etc/hosts: 127.0.0.1	capifcore


##### Set environment variables 
capifhost="capifcore"
capifhttpport="8080"

exposerpk="-----BEGIN CERTIFICATE REQUEST-----\nMIIC0TCCAbkCAQAwgYsxEDAOBgNVBAMMB2V4cG9zZXIxFzAVBgNVBAoMDlRlbGVm\nb25pY2EgSStEMRMwEQYDVQQLDApJbm5vdmF0aW9uMQ8wDQYDVQQHDAZNYWRyaWQx\nDzANBgNVBAgMBk1hZHJpZDELMAkGA1UEBhMCRVMxGjAYBgkqhkiG9w0BCQEWC2lu\nbm9AdGlkLmVzMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkpJ7FzAI\nkzFYxLKbW54lIsQBNIQz5zQIvRZDFcrO4QLR2jQUps9giBWEDih++47JiBJyM+z1\nWkEh7b+moZhQThj7L9PKgJHRhU1oeHpSE1x/r7479J5F+CFRqFo5v9dC+2zGfP4E\nsSrNfp3MK/KQHsHhMzSt881xAHs+p2/bcM+sd/BlXC4J6E1y6Hk3ogI7kq443fcY\noUHZx9ClUSboOvXa1ZSPVxdCV6xKRraUdAKfhMGn+pYtJDsNp8Gg/BN8NXmYUzl9\ntDhjeuIxr4N38LgW3gRHLNIa8acO9eBctWw9AD20JWzFAXvvmsboBPc2wsOVcsml\ncCbisMRKX4JyKQIDAQABoAAwDQYJKoZIhvcNAQELBQADggEBAIxZ1Sec9ATbqjhi\nRz4rvhX8+myXhyfEw2MQ62jz5tpH4qIVZFtn+cZvU/ULySY10WHaBijGgx8fTaMh\nvjQbc+p3PXmgtnmt1QmoOGjDTFa6vghqpxPLSUjjCUe8yj5y24gkOImY6Cv5rzzQ\nlnTMkNvnGgpDgUeiqWcQNbwwge3zkzp9bVRgogTT+EDxiFnjTTF6iUG80sRtXMGr\nD6sygLsF2zijGGfWoKRo/7aZTQxuCiCixceVFXegMfr+eACkOjV25Kso7hYBoEdP\nkgUf5PNpl5uK3/rmPIrl/TeE0SnGGfCYP7QajE9ELRsBVmVDZJb7ZxUl1A4YydFY\ni0QOM3Y=\n-----END CERTIFICATE REQUEST-----\n"


##### Retrieve and store CA certificate 

curl --request GET "http://$capifhost:$capifhttpport/ca-root" 2>/dev/null | jq -r '.certificate' -j > ca.crt


##### Register an entity 

exposerid=$(curl --request POST "http://$capifhost:$capifhttpport/register" --header 'Content-Type: application/json' --data '{
    "username":"exposer",
    "password":"exposer",
    "role":"exposer",
    "description":"Exposer",
    "cn":"exposer"
}' 2>/dev/null | jq -r '.id' -j)


##### Get access token

exposertoken=$(curl --request POST "http://$capifhost:$capifhttpport/gettoken" --header 'Content-Type: application/json' --data '{
    "username":"exposer",
    "password":"exposer",
    "role":"exposer"
}' 2>/dev/null | jq -r '.access_token' -j)


##### Sign exposer certificate

curl --request POST "http://$capifhost:$capifhttpport/sign-csr" --header "Authorization: Bearer $exposertoken" --header 'Content-Type: application/json' --data-raw "{
  \"csr\":  \"$exposerpk\",
  \"mode\":  \"client\",
  \"filename\": \"exposer\"
}" 2>/dev/null | jq -r '.certificate' -j > exposer.crt


##### Publish service
curl --cert exposer.crt --key exposer.key --cacert ca.crt --request POST "https://$capifhost/published-apis/v1/$exposerid/service-apis"  --header 'Content-Type: application/json' --data '{
  "apiName": "3gpp-monitoring-event",
  "aefProfiles": [
    {
      "aefId": "string",
      "versions": [
        {
          "apiVersion": "v1",
          "expiry": "2021-11-30T10:32:02.004Z",
          "resources": [
            {
              "resourceName": "string",
              "commType": "REQUEST_RESPONSE",
              "uri": "string",
              "custOpName": "string",
              "operations": [
                "GET"
              ],
              "description": "string"
            }
          ],
          "custOperations": [
            {
              "commType": "REQUEST_RESPONSE",
              "custOpName": "string",
              "operations": [
                "GET"
              ],
              "description": "string"
            }
          ]
        }
      ],
      "protocol": "HTTP_1_1",
      "dataFormat": "JSON",
      "securityMethods": ["PSK"],
      "interfaceDescriptions": [
        {
          "ipv4Addr": "string",
          "port": 65535,
          "securityMethods": ["PSK"]
        },
        {
          "ipv4Addr": "string",
          "port": 65535,
          "securityMethods": ["PSK"]
        }
      ]
    }
  ],
  "description": "string",
  "supportedFeatures": "fffff",
  "shareableInfo": {
    "isShareable": true,
    "capifProvDoms": [
      "string"
    ]
  },
  "serviceAPICategory": "string",
  "apiSuppFeats": "fffff",
  "pubApiPath": {
    "ccfIds": [
      "string"
    ]
  },
  "ccfId": "string"
}' > response.json

apiserviceid=$(cat response.json | jq -r '.apiId' -j)


##### Update a published service API
curl --cert exposer.crt --key exposer.key --cacert ca.crt --request PUT "https://$capifhost/published-apis/v1/$exposerid/service-apis/$apiserviceid" --header 'Content-Type: application/json' --data '{
  "apiName": "3gpp-monitoring-event",
  "aefProfiles": [
    {
      "aefId": "string1",
      "versions": [
        {
          "apiVersion": "v1",
          "expiry": "2021-11-30T10:32:02.004Z",
          "resources": [
            {
              "resourceName": "string",
              "commType": "REQUEST_RESPONSE",
              "uri": "string",
              "custOpName": "string",
              "operations": [
                "GET"
              ],
              "description": "string"
            }
          ],
          "custOperations": [
            {
              "commType": "REQUEST_RESPONSE",
              "custOpName": "string",
              "operations": [
                "GET"
              ],
              "description": "string"
            }
          ]
        }
      ],
      "protocol": "HTTP_1_1",
      "dataFormat": "JSON",
      "securityMethods": ["PSK"],
      "interfaceDescriptions": [
        {
          "ipv4Addr": "string",
          "port": 65535,
          "securityMethods": ["PSK"]
        },
        {
          "ipv4Addr": "string",
          "port": 65535,
          "securityMethods": ["PSK"]
        }
      ]
    }
  ],
  "description": "string",
  "supportedFeatures": "fffff",
  "shareableInfo": {
    "isShareable": true,
    "capifProvDoms": [
      "string"
    ]
  },
  "serviceAPICategory": "string",
  "apiSuppFeats": "fffff",
  "pubApiPath": {
    "ccfIds": [
      "string"
    ]
  },
  "ccfId": "string"
}'


##### Retrieve all published APIs

curl --cert exposer.crt --key exposer.key --cacert ca.crt --request GET "https://$capifhost/published-apis/v1/$exposerid/service-apis"


##### Retrieve a published service API

curl --cert exposer.crt --key exposer.key --cacert ca.crt --request GET "https://$capifhost/published-apis/v1/$exposerid/service-apis/$apiserviceid"


##### Unpublish a published service API

curl --cert exposer.crt --key exposer.key --cacert ca.crt --request DELETE "https://$capifhost/published-apis/v1/$exposerid/service-apis/$apiserviceid"


