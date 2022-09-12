- [Repository structure](#repository-structure)
- [CAPIF_API_Services](#capif_api_services)
  - [How to run CAPIF services in this Repository](#how-to-run-capif-services-in-this-repository)
    - [Run All CAPIF Services locally with Docker images](#run-all-capif-services-locally-with-docker-images)
    - [Run each service using Docker](#run-each-service-using-docker)
    - [Run each service using Python](#run-each-service-using-python)
- [How to test CAPIF APIs](#how-to-test-capif-apis)
  - [Robot Framework](#robot-framework)
    - [Test Plan Documentation](#test-plan-documentation)
    - [Previously Steps](#previously-steps)
    - [Tests Execution](#tests-execution)
    - [Test result review](#test-result-review)
  - [Using Curl](#using-curl)
    - [Authentication](#authentication)
      - [Invoker](#invoker)
      - [Exposer](#exposer)
    - [JWT Authentication APIs](#jwt-authentication-apis)
      - [Register an entity](#register-an-entity)
      - [Get access token for an existing entity](#get-access-token-for-an-existing-entity)
      - [Retrieve and store CA certificate](#retrieve-and-store-ca-certificate)
      - [Sign exposer certificate](#sign-exposer-certificate)
    - [Invoker Management APIs](#invoker-management-apis)
      - [Onboard an Invoker](#onboard-an-invoker)
      - [Update Invoker Details](#update-invoker-details)
      - [Offboard an Invoker](#offboard-an-invoker)
    - [Publish APIs](#publish-apis)
      - [Publish a new API.](#publish-a-new-api)
      - [Update a published service API.](#update-a-published-service-api)
      - [Unpublish a published service API.](#unpublish-a-published-service-api)
      - [Retrieve all published APIs](#retrieve-all-published-apis)
      - [Retrieve a published service API.](#retrieve-a-published-service-api)
    - [Discover API](#discover-api)
      - [Discover published service APIs and retrieve a collection of APIs according to certain filter criteria.](#discover-published-service-apis-and-retrieve-a-collection-of-apis-according-to-certain-filter-criteria)
  - [Using PostMan (only for release 1.0 of CAPIF)](#using-postman-only-for-release-10-of-capif)
  - [Using cURL (TLS supported)](#using-curl-tls-supported)
- [Important urls:](#important-urls)
  - [Mongo DB Dashboard](#mongo-db-dashboard)
- [CAPIF Tool Release 1.0](#capif-tool-release-10)
- [CAPIF Tool Release 2.0](#capif-tool-release-20)


# Repository structure

```
CAPIF_API_Services
└───docs
│    └───test_plan
│    └───testing_with_postman
└───iac
│    └───terraform
└───pac
└───services
└───tests
└───tools
    └───robot
    └───open_api_script
```
* **services**: Services developed following CAPIF API specifications. Also, other complementary services (e.g., NGINX and JWTauth services for the authentication of API consuming entities).
* **tools**: Auxiliary tools. Robot Framework related code and OpenAPI scripts.
* **test**: Tests developed using Robot Framework.

* **docs**: Documents related to the code in the repository.
  * images: images used in the repository
  * test_plan: test plan descriptions for each API service referring to the test that are executed with the Robot Framework.
  * testing_with_postman: auxiliary JSON file needed for the Postman-based examples.
* **iac**: Infrastructure as Code, contains all the files needed for the deployment of the structure that supports the services. (It is used only for the case of non-local deployment of the CCF services e.g., in the Openshift of EVOLVED-5G project)).
    * Terraform: Deploy file.
* **pac**: Jenkins files to manage different automated tasks. (It is used only for the case of non-local deployment of the CCF services e.g., in the Openshift of EVOLVED-5G project).
  * Jenkins Pipelines.

# CAPIF_API_Services
This repository has the python-flask Mockup servers created with openapi-generator related with CAPIF APIS defined here:
https://github.com/jdegre/5GC_APIs

## How to run CAPIF services in this Repository
Capif services are developed under /service/ folder.

### Run All CAPIF Services locally with Docker images
To run using docker and docker-compose you must ensure you have that tools installed at your machine. Also to simplify the process, we have 3 script to control docker images to deploy, check and cleanup.

To run all CAPIF APIs locally using docker and docker-compose you can execute:
```
cd services/

./run.sh
```
This will build and run all services using docker images, including mongodb and nginx locally and in background, and import ca.crt to nginx.

Nginx deployed by default use capifcore hostname, but can add a parameter when run.sh is executed setting a different hostname, for example,
```
./run.sh openshift.evolved-5g.eu
```

If you want to check if all CAPIF services are running properly in local machine after execute run.sh, we can use:
```
./check_services_are_running.sh
```
This shell script will return 0 if all services are running properly.

When we need to stop CAPIF services, we can use next bash script:
```
./clean_capif_docker_services.sh
```
This shell script will remove and clean all CAPIF services started previously with run.sh

### Run each service using Docker

Also you can run service by service using docker:
```
cd <Service>
docker build -t capif_security .
docker run -p 8080:8080 capif_security
```

### Run each service using Python

Run using python
```
cd <Service>
pip3 install -r requirements.txt
python3 -m <service>
```

# How to test CAPIF APIs
The above APIs can be tested either with "curl" command, POSTMAN tool or running developed tests with Robot Framework.
## Robot Framework

In order to ensure modifications over CAPIF services still accomplish the required functionallity, Robot Framework test suite must be success.

Test suite implemented accomplish requirements described under test plan at /docs/test_plan/ folder.
### Test Plan Documentation

Complete documentation of tests is here: [Test Plan Directory](./docs/test_plan/README.md)

### Previously Steps
In order run test plan, the easiest way is build robot docker image using dockerfile under /tools/robot. Requirements:
* Docker installed and running in local machine.

Steps to execute test plan:
* **Build Robot docker image**:
```
cd tools/robot
docker build . -t 5gnow-robot-test:latest
```
* **Run All Services**: See section [Run All CAPIF Services](#run-all-capif-services-locally-with-docker-images)

### Tests Execution
  
Execute all tests locally:
```
<PATH_TO_REPOSITORY>=path in local machine to repository cloned.
<PATH_RESULT_FOLDER>=path to a folder on local machine to store results of Robot Framework execution.
<CAPIF_HOSTNAME>=Is the hostname set when run.sh is executed, by default it will be capifcore.
<CAPIF_HTTP_PORT>=This is the port to reach when robot framework want to reach CAPIF deployment using http, this should be set to port without TLS set on Nginx, 8080 by default.

To execute all tests run :
docker run -ti --rm --network="host" -v <PATH_TO_REPOSITORY>/tests:/opt/robot-tests/tests -v <PATH_RESULT_FOLDER>:/opt/robot-tests/results 5gnow-robot-test:latest --variable CAPIF_HOSTNAME:capifcore --variable CAPIF_HTTP_PORT:8080 --include all
```

Execute specific tests locally:
```
To run more specific tests, for example, only one functionality:
<TAG>=Select one from list:
  "capif_api_discover_service",
  "capif_api_invoker_management",
  "capif_api_publish_service",
  "capif_api_events",
  "capif_security_api

And Run:
docker run -ti --rm --network="host" -v <PATH_TO_REPOSITORY>/tests:/opt/robot-tests/tests -v <PATH_RESULT_FOLDER>:/opt/robot-tests/results 5gnow-robot-test:latest --variable CAPIF_HOSTNAME:capifcore --variable CAPIF_HTTP_PORT:8080 --include <TAG>
```
### Test result review

In order to Review results after tests, you can check general report at <PATH_RESULT_FOLDER>/report.html or if you need more detailed information <PATH_RESULT_FOLDER>/log.html, example:
* Report:
![Report](docs/images/robot_report_example.png)
* Detailed information:
![Log](docs/images/robot_log_example.png)
## Using Curl
### Authentication
This version will use TLS communication, for that purpose we have 2 different scenarios, according to role:
* Invoker
* Exposer

#### Invoker
To authenticate an invoker user, we must perform next steps:
- Retrieve CA certificate from platform. [Retrieve and store CA certificate](#retrieve-and-store-ca-certificate)
- Register on the CAPIF with invoker role. [Register an entity](#register-an-entity)
- Get a Json Web Token (JWT) in order to request onboarding [Get access token for an existing entity](#get-access-token-for-an-existing-entity)
- Request onboarding adding public key to request. [Onboard an Invoker](#onboard-an-invoker)
- Store certificate signed by CAPIF platform to allow TLS onwards.

Flow:
![Flow](docs/images/invoker_onboarding_flow.png)

#### Exposer
To authenticate an exposer user, we must perform next steps:
- Retrieve CA certificate from platform. [Retrieve and store CA certificate](#retrieve-and-store-ca-certificate)
- Register on the CAPIF with exposer role. [Register an entity](#register-an-entity)
- Request sign the public key to CAPIF including beared with JWT. [Sign exposer certificate](#sign-exposer-certificate)
- Store certificate signed by CAPIF platform to allow TLS onwards.

Flow:
![Flow](docs/images/publisher_registry_flow.png)

### JWT Authentication APIs
These APIs are triggered by an entity (Invoker or Exposer for release 1.0) to:
- register on the CAPIF Framework
- get a Json Web Token (JWT) in order to be authorized to call CAPIF APIs

#### Register an entity
Request
```shell
curl --request POST 'http://<CAPIF_HOSTNAME>:<CAPIF_HTTP_PORT>/register' --header 'Content-Type: application/json' --data '{
    "username":"...",
    "password":"...",
    "role":"...",
    "description":"...",
    "cn":"..."
}'
```

* Role: invoker or publisher
* cn: common name

Response body
```json
{
  "id": "Entity ID",
  "message": "Informative message"
}
```

#### Get access token for an existing entity
Request
```shell
curl --request POST 'http://<CAPIF_HOSTNAME>:<CAPIF_HTTP_PORT>/gettoken' --header 'Content-Type: application/json' --data '{
    "username":"...",
    "password":"...",
    "role":"..."
}'
```

Response body
```json
{
  "access_token": "JSON Web Token for CAPIF APIs", 
  "message": "Informative message"
}
```

#### Retrieve and store CA certificate
```shell
curl --request GET 'http://<CAPIF_HOSTNAME>:<CAPIF_HTTP_PORT>/ca-root' 2>/dev/null | jq -r '.certificate' -j > <CA Certificate file>
```

#### Sign exposer certificate
```shell
curl --request POST 'http://<CAPIF_HOSTNAME>/sign-csr' --header 'Authorization: Bearer <JWT access token>' --header 'Content-Type: application/json' --data-raw '{
  "csr":  "RAW PUBLIC KEY CREATED BY PUBLISHER",
  "mode":  "client",
  "filename": exposer
}'
```
Response
``` json
{
  "certificate": "PUBLISHER CERTIFICATE"
}
```
PUBLISHER CERTIFICATE value must be stored by Exposer entity to next request to CAPIF (exposer.crt for example)

### Invoker Management APIs

These APIs are triggered by a NetApp (i.e. Invoker)

#### Onboard an Invoker

```shell
curl --cacert <CA Certificate file> --request POST 'https://<CAPIF_HOSTNAME>/api-invoker-management/v1/onboardedInvokers' --header 'Authorization: Bearer <Invoker JWT access token>' --header 'Content-Type: application/json' --data-raw '{
  "notificationDestination" : "http://X:Y/netapp_callback",
  "supportedFeatures" : "fffffff",
  "apiInvokerInformation" : <Invoker CommonName>,
  "websockNotifConfig" : {
    "requestWebsocketUri" : true,
    "websocketUri" : "websocketUri"
  },
  "onboardingInformation" : {
    "apiInvokerPublicKey" : <RAW PUBLIC KEY CREATED BY INVOKER>
  },
  "requestTestNotification" : true
}'
```

Response Body

``` json
{
  "apiInvokerId": "7da0a8d4172d7d86c536c0fbc9c372",
  "onboardingInformation": {
    "apiInvokerPublicKey": "RAW PUBLIC KEY CREATED BY INVOKER", 
    "apiInvokerCertificate": "INVOKER CERTIFICATE", 
    "onboardingSecret": "onboardingSecret"
    }, 
    "notificationDestination": "http://host.docker.internal:8086/netapp_callback", 
    "requestTestNotification": true, 
    ...
}
```

INVOKER CERTIFICATE value must be stored by Invoker entity to next request to CAPIF (invoker.crt for example)

#### Update Invoker Details

```shell
curl --location --request PUT 'https://<CAPIF_HOSTNAME>/api-invoker-management/v1/onboardedInvokers/<API Invoker ID>' --cert <Invoker Signed Certificate file> --key <Invoker Private Key> --cacert <CA Certificate file> --header 'Content-Type: application/json' --data '{
  "notificationDestination" : "http://X:Y/netapp_callback2",
  "supportedFeatures" : "fffffff",
  "apiInvokerInformation" : <Invoker CommonName>,
  "websockNotifConfig" : {
    "requestWebsocketUri" : true,
    "websocketUri" : "websocketUri2"
  },
  "onboardingInformation" : {
    "apiInvokerPublicKey" : <RAW PUBLIC KEY CREATED BY INVOKER>
  },
  "requestTestNotification" : true
}'
```

#### Offboard an Invoker

```shell
curl --cert <Invoker Signed Certificate file> --key <Invoker Private Key> --cacert <CA Certificate file> --request DELETE 'https://<CAPIF_HOSTNAME>/api-invoker-management/v1/onboardedInvokers/<API Invoker ID>' 
```

### Publish APIs

These APIs are triggered by the API Publishing Function (APF) of an Exposer

#### Publish a new API.
```shell
curl --cert <Exposer Signed Certificate file> --key <Exposer Private Key> --cacert <CA Certificate file> --request POST 'https://<CAPIF_HOSTNAME>/published-apis/v1/<Exposer Id>/service-apis'  --header 'Content-Type: application/json' --data '{
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
}'
```

#### Update a published service API.
```shell
curl --cert <Exposer Signed Certificate file> --key <Exposer Private Key> --cacert <CA Certificate file> --request PUT 'https://<CAPIF_HOSTNAME>/published-apis/v1/<APIF Id>/service-apis/<Service API Id>' --header 'Content-Type: application/json' --data '{
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
```

#### Unpublish a published service API.
```shell
curl --cert <Exposer Signed Certificate file> --key <Exposer Private Key> --cacert <CA Certificate file> --request DELETE 'https://<CAPIF_HOSTNAME>/published-apis/v1/<APF Id>/service-apis/<Service API Id>'
```

#### Retrieve all published APIs
```shell
curl --cert <Exposer Signed Certificate file> --key <Exposer Private Key> --cacert <CA Certificate file> --request GET 'https://<CAPIF_HOSTNAME>/published-apis/v1/<APF Id>/service-apis'
```

#### Retrieve a published service API.
```shell
curl --cert <Exposer Signed Certificate file> --key <Exposer Private Key> --cacert <CA Certificate file> --request GET 'https://<CAPIF_HOSTNAME>/published-apis/v1/<APF Id>/service-apis/<Service API Id>'
```

### Discover API

This API is triggered by a NetApp (or Invoker)

#### Discover published service APIs and retrieve a collection of APIs according to certain filter criteria.
```shell
curl --cert <Invoker Signed Certificate file> --key <Invoker Private Key> --cacert <CA Certificate file> --request GET 'https://<CAPIF_HOSTNAME>/service-apis/v1/allServiceAPIs?api-invoker-id=<API Invoker Id>&api-name=<API Name>&api-version=<API version e.g. v1>&aef-id=<AEF Id>&api-cat=<Service API Category>&supported-features=<SuppFeat>&api-supported-features=<API Suppfeat>'
```


## Using PostMan (only for release 1.0 of CAPIF)
For more information on how to test the APIs with POSTMAN, follow this [Document](docs/testing_with_postman/EVOLVED-5G%20--%20using%20CCF%20from%20Postman_13.1.2022.pdf).
Also you have here the [POSTMAN Collection](docs/testing_with_postman/CAPIF_export_APIs.postman_collection.json) **TLS NOT ADDED**

## Using cURL (TLS supported)
Follow the instructions and run the commands of the bash scripts in [here](docs/testing_with_curl) to test CAPIF with TLS support.

# Important urls:

## Mongo DB Dashboard
```
http://0.0.0.0:8082/ (if accessed from localhost) 

or

http://<Mongo Express Host IP>:8082/ (if accessed from another host)
```


# CAPIF Tool Release 1.0

The APIs included in release 1.0 are:
- JWT Authentication APIs
- CAPIF Invoker Management API
- CAPIF Publish API
- CAPIF Discover API
- CAPIF Security API
- CAPIF Events API
  

# CAPIF Tool Release 2.0

This release includes CAPIF Provider Management API and also TLS communication. For TLS communication Easy RSA server was developed, in order to sign certificates.

The APIs included in release 2.0 are:
- CAPIF Invoker Management API
- CAPIF Publish API
- CAPIF Discover API
- CAPIF Security API
- CAPIF Events API
- CAPIF Provider Management API

Additional information about this version:
- JWT Authentication Server
- Easy RSA Server
- TLS Enabled
