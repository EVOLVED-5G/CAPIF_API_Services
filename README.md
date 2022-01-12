# CAPIF_API_Services
This repository has the python-flask Mockup servers created with openapi-generator related with CAPIF APIS defined here:
https://github.com/jdegre/5GC_APIs

# How to run CAPIF services in this Repository

## Run All CAPIF Services locally with Docker images

To run using docker and docker-compose you must ensure you have that tools installed at your machine. Also to simplify the process, we have 3 script to control docker images to deploy, check and cleanup.

To run all CAPIF APIs locally using docker and docker-compose you can execute:
```
cd services/

./run.sh
```
This will build and run all services using docker images, including mongodb and nginx locally and in background.

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

## Run each service using Docker

Also you can run service by service using docker:
```
cd <Service>
docker build -t openapi_server .
docker run -p 8080:8080 openapi_server
```

## Run each service using Python

Run using python
```
cd <Service>
pip3 install -r requirements.txt
python3 -m <service>
```

# CAPIF Tool Release 1.0

The APIs included in release 1.0 are:
- JWT Authentication APIs
- CAPIF Invoker Management API
- CAPIF Publish API
- CAPIF Discover API


### The above APIs can be tested either with "curl" command or with POSTMAN tool. Below we present how to test the APIs with "curl". 
### For more information on how to test the APIs with POSTMAN, follow this [link]()


## JWT Authentication APIs

These APIs are triggered by an entity (Invoker or APF for release 1.0) to:
- register on the CAPIF Framework
- get a Json Web Token (JWT) in order to be authorized to call CAPIF APIs

### Register an entity
Request
```shell
curl --request POST 'http://localhost:8080/register' --header 'Content-Type: application/json' --data '{
    "username":"...",
    "password":"...",
    "role":"...",
    "description":"..."
}'
```

Response body
```json
{
  "id": "Entity ID",
  "message": "Informative message"
}
```

### Get access token for an existing entity
Request
```shell
curl --request POST 'http://localhost:8080/gettoken' --header 'Content-Type: application/json' --data '{
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

## Invoker Management APIs

These APIs are triggered by a NetApp (i.e. Invoker)

### Onboard an Invoker

```shell
curl --request POST 'http://localhost:8080/api-invoker-management/v1/onboardedInvokers' --header 'Authorization: Bearer <JWT access token>' --header 'Content-Type: application/json' --data-raw '{
  "notificationDestination" : "notificationDestination",
  "supportedFeatures" : "fffffff",
  "onboardingInformation" : {
    "apiInvokerPublicKey" : "apiInvokerPublicKey1",
    "onboardingSecret" : "onboardingSecret1",
    "apiInvokerCertificate" : "apiInvokerCertificate1"
  },
  "apiList" : [ {
    "serviceAPICategory" : "serviceAPICategory",
    "ccfId" : "ccfId",
    "apiName" : "apiName",
    "shareableInfo" : {
      "capifProvDoms" : [ "capifProvDoms", "capifProvDoms" ],
      "isShareable" : true
    },
    "supportedFeatures" : "fffffff",
    "apiSuppFeats" : "fffffff",
    "apiId" : "apiId",
    "aefProfiles" : [ {
      "securityMethods" : ["PSK"],
      "versions" : [ {
        "apiVersion" : "apiVersion",
        "resources" : [ {
          "operations" : ["GET"],
          "description" : "description",
          "resourceName" : "resourceName",
          "custOpName" : "custOpName",
          "uri" : "uri",
          "commType": "REQUEST_RESPONSE"
        }, {
          "operations" : ["GET"],
          "description" : "description",
          "resourceName" : "resourceName",
          "custOpName" : "custOpName",
          "uri" : "uri",
          "commType": "REQUEST_RESPONSE"
        } ],
        "custOperations" : [ {
          "operations" : ["GET"],
          "description" : "description",
          "custOpName" : "custOpName",
          "commType" : "REQUEST_RESPONSE"
        }, {
          "operations" : ["GET"],
          "description" : "description",
          "custOpName" : "custOpName",
          "commType" : "REQUEST_RESPONSE"
        } ],
        "expiry" : "2000-01-23T04:56:07.000+00:00"
      } ],
      "aefId" : "aefId",
      "interfaceDescriptions" : [ {
        "securityMethods" : ["PSK"],
        "port" : 5248,
        "ipv4Addr" : "ipv4Addr"
      } ]
    } ],
    "pubApiPath" : {
      "ccfIds" : [ "ccfIds", "ccfIds" ]
    }
  } ]
}'
```

### Update Invoker Details

```shell
curl --location --request PUT 'http://localhost:8080/api-invoker-management/v1/onboardedInvokers/<API Invoker ID>' --header 'Authorization: Bearer <JWT access token>' --header 'Content-Type: application/json' --data '{
  "notificationDestination" : "notificationDestination1",
  "supportedFeatures" : "fffffff",
  "onboardingInformation" : {
    "apiInvokerPublicKey" : "apiInvokerPublicKey1",
    "onboardingSecret" : "onboardingSecret1",
    "apiInvokerCertificate" : "apiInvokerCertificate1"
  },
  "apiList" : [ {
    "serviceAPICategory" : "serviceAPICategory",
    "ccfId" : "ccfId",
    "apiName" : "apiName",
    "shareableInfo" : {
      "capifProvDoms" : [ "capifProvDoms", "capifProvDoms" ],
      "isShareable" : true
    },
    "supportedFeatures" : "fffffff",
    "apiSuppFeats" : "fffffff",
    "apiId" : "apiId",
    "aefProfiles" : [ {
      "securityMethods" : ["PSK"],
      "versions" : [ {
        "apiVersion" : "apiVersion",
        "resources" : [ {
          "operations" : ["GET"],
          "description" : "description",
          "resourceName" : "resourceName",
          "custOpName" : "custOpName",
          "uri" : "uri",
          "commType": "REQUEST_RESPONSE"
        }, {
          "operations" : ["GET"],
          "description" : "description",
          "resourceName" : "resourceName",
          "custOpName" : "custOpName",
          "uri" : "uri",
          "commType": "REQUEST_RESPONSE"
        } ],
        "custOperations" : [ {
          "operations" : ["GET"],
          "description" : "description",
          "custOpName" : "custOpName",
          "commType" : "REQUEST_RESPONSE"
        }, {
          "operations" : ["GET"],
          "description" : "description",
          "custOpName" : "custOpName",
          "commType" : "REQUEST_RESPONSE"
        } ],
        "expiry" : "2000-01-23T04:56:07.000+00:00"
      } ],
      "aefId" : "aefId",
      "interfaceDescriptions" : [ {
        "securityMethods" : ["PSK"],
        "port" : 5248,
        "ipv4Addr" : "ipv4Addr"
      } ]
    } ],
    "pubApiPath" : {
      "ccfIds" : [ "ccfIds", "ccfIds" ]
    }
  } ]
}'
```

### Offboard an Invoker

```shell
curl --request DELETE 'http://localhost:8080/api-invoker-management/v1/onboardedInvokers/<API Invoker ID>' --header 'Authorization: Bearer <JWT access token>'
```

## Publish APIs

These APIs are triggered by an API Publishing Function (APF)

### Publish a new API.
```shell
curl --request POST 'http://localhost:8080/published-apis/v1/<APF Id>/service-apis' --header 'Authorization: Bearer <JWT access token>' --header 'Content-Type: application/json' --data '{
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

### Update a published service API.
```shell
curl --request PUT 'http://localhost:8080/published-apis/v1/<APIF Id>/service-apis/<Service API Id>' --header 'Authorization: Bearer <JWT access token>' --header 'Content-Type: application/json' --data '{
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

### Unpublish a published service API.
```shell
curl --request DELETE 'http://localhost:8080/published-apis/v1/<APF Id>/service-apis/<Service API Id>' --header 'Authorization: Bearer <JWT access token>'
```

### Retrieve all published APIs
```shell
curl --request GET 'http://localhost:8080/published-apis/v1/<APF Id>/service-apis' --header 'Authorization: Bearer <JWT access token>'
```

### Retrieve a published service API.
```shell
curl --request GET 'http://localhost:8080/published-apis/v1/<APF Id>/service-apis/<Service API Id>' --header 'Authorization: Bearer <JWT access token>'
```

## Discover API

This API is triggered by a NetApp (or Invoker)

### Discover published service APIs and retrieve a collection of APIs according to certain filter criteria.
```shell
curl --request GET 'http://localhost:8080/service-apis/v1/allServiceAPIs?api-invoker-id=<API Invoker Id>&api-name=<API Name>&api-version=<API version e.g. v1>&aef-id=<AEF Id>&api-cat=<Service API Category>&supported-features=<SuppFeat>&api-supported-features=<API Suppfeat>' --header 'Authorization: Bearer <JWT acces token>'
```

# Test Plan Documentation

[Test Plan Directory](./docs/test_plan/README.md)



# Important urls:

## Mongo DB Dashboard
```
http://0.0.0.0:8082/ (if accessed from localhost) 

or

http://<Mongo Express Host IP>:8082/ (if accessed from another host)
```

```

CAPIF_API_Services
└───docs
└───iac
└───pac
└───services
└───tests
└───tools
```

* docs: Documents related with this proyect, like test plans, ppts...
* iac: Infrastructure as Code, contains all files needed to deploy the structure that support services.
* pac: Jenkins files to manage different automated tasks
* services: Services developed following CAPIF specifications, and also come other complementary services.
* test: Tests developed using Robot Framework
* tools: Auxiliary tools



```

CAPIF_API_Services
└───docs
│   └───test_plan
│       │   README.md
│       └───api_discover_service
│       │   │   test_plan.md
│       └───api_events_service
│       │   │   test_plan.md
│       └───api_invoker_management
│       │   │   test_plan.md
│       └───api_provider_management
│       │   │   test_plan.md
│       └───api_publish_service
│       │   │   test_plan.md
│       └───api_security_service
│           │   test_plan.md
│   
└───iac
│   └───terraform
└───pac
└───services
└───tests
└───tools
    └───robot
    └───open_api_script
```