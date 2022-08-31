##### Execute Invoker curls locally

##### Configure machine 

##### Add in /etc/hosts: 127.0.0.1	capifcore


##### Set environment variables

capifhost="capifcore"
capifhttpport="8080"

invokerpk="-----BEGIN CERTIFICATE REQUEST-----\nMIIC0TCCAbkCAQAwgYsxEDAOBgNVBAMMB2ludm9rZXIxFzAVBgNVBAoMDlRlbGVm\nb25pY2EgSStEMRMwEQYDVQQLDApJbm5vdmF0aW9uMQ8wDQYDVQQHDAZNYWRyaWQx\nDzANBgNVBAgMBk1hZHJpZDELMAkGA1UEBhMCRVMxGjAYBgkqhkiG9w0BCQEWC2lu\nbm9AdGlkLmVzMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArfITEb3/\nJ5KDt7ia2WsQrd8iSrlH8kh6D9YNPEF+KaIGQ9w8QhmOW416uvIAASzOaCKMNqgb\nCI0NqsbVF9lfaiBgB71vcwX0yKatjACn3Nl3Lnubi+tH4Jb5zGQQXOuxpMHMmgyn\nNTsSc/MeMzX3iUWqLmmhnTC31Mu1ESUPTBa+CitQAj2wYMvBS970WICKrDlxWkR8\nZZBkRBZaxMfqY21VWmREtR+Kl6GCMBtUCUBH6uWjFiOpxYbCxdygxxrA4a3IzmiO\ntXOyLs7iuOP/CLSYfk71MHX2qKlpAyjdRK2W0w0GioV90Hk4uT/YUYy9zjWWN+mm\nrQ9GBy8iRZm7YwIDAQABoAAwDQYJKoZIhvcNAQELBQADggEBAI0btA7KDMvkY4Ib\n0eMteeeT40bm11Yw8/6V48IaIPi9EpZMI+jWyCebw8PBFUs3l3ImWeO8Gma96gyf\np0WB/64MRkUSdOxUWOWGMPIMEF+BH3eiHthx+EbAETtJ0D4KzmH6raxl14qvwLS5\nwxtxPGxu/R5ue5RVJpAzzJ6OX36p05GYSzL+pTotVPpowSdoeNsV+xPgPA0diV8a\nB7Zn/ujwMpsh7IjQPKpOEkhQdxc478Si8dmRbzXkVar1Oa8/QSJ8ZAaFI4VGowjR\nmtxps7AvS5OG9iMPtFQHpqxHVO50CJU5cbsXsYdu9EipGhgIKJDKewBX7tCKk0Ot\nBLU03CY=\n-----END CERTIFICATE REQUEST-----\n"


##### Retrieve and store CA certificate

curl --request GET "http://$capifhost:$capifhttpport/ca-root" 2>/dev/null | jq -r '.certificate' -j > ca.crt


##### Register an entity 

invokerid=$(curl --request POST "http://$capifhost:$capifhttpport/register" --header 'Content-Type: application/json' --data '{
    "username":"invoker",
    "password":"invoker",
    "role":"invoker",
    "description":"Invoker",
    "cn":"invoker"
}' 2>/dev/null | jq -r '.id' -j)


##### Get access token 

invokertoken=$(curl --request POST "http://$capifhost:$capifhttpport/gettoken" --header 'Content-Type: application/json' --data '{
    "username":"invoker",
    "password":"invoker",
    "role":"invoker"
}' 2>/dev/null | jq -r '.access_token' -j)


##### Onboard an Invoker 

curl --cacert ca.crt --request POST "https://$capifhost/api-invoker-management/v1/onboardedInvokers" --header "Authorization: Bearer $invokertoken" --header 'Content-Type: application/json' --data-raw "{
  \"notificationDestination\" : \"http://X:Y/netapp_callback\",
  \"supportedFeatures\" : \"fffffff\",
  \"apiInvokerInformation\" : \"invoker\",
  \"websockNotifConfig\" : {
    \"requestWebsocketUri\" : true,
    \"websocketUri\" : \"websocketUri\"
  },
  \"onboardingInformation\" : {
    \"apiInvokerPublicKey\" : \"$invokerpk\"
  },
  \"requestTestNotification\" : true
}" > response.json

cat response.json | jq -r '.onboardingInformation.apiInvokerCertificate' -j > invoker.crt
apiinvokerid=$(cat response.json | jq -r '.apiInvokerId' -j)


##### Update Invoker Details 

curl --location --request PUT "https://$capifhost/api-invoker-management/v1/onboardedInvokers/$apiinvokerid" --cert invoker.crt --key invoker.key --cacert ca.crt --header 'Content-Type: application/json' --data "{
  \"notificationDestination\" : \"http://X:Y/netapp_callback2\",
  \"supportedFeatures\" : \"fffffff\",
  \"apiInvokerInformation\" : \"test\",
  \"websockNotifConfig\" : {
    \"requestWebsocketUri\" : true,
    \"websocketUri\" : \"websocketUri2\"
  },
  \"onboardingInformation\" : {
    \"apiInvokerPublicKey\" : \"$invokerpk\"
  },
  \"requestTestNotification\" : true
}"


##### Discover API 

curl --cert invoker.crt --key invoker.key --cacert ca.crt --request GET "https://$capifhost/service-apis/v1/allServiceAPIs?api-invoker-id=$apiinvokerid"


##### Offboard an Invoker 

curl --cert invoker.crt --key invoker.key --cacert ca.crt --request DELETE "https://$capifhost/api-invoker-management/v1/onboardedInvokers/$apiinvokerid"

