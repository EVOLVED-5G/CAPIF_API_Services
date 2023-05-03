# Common API Framework (CAPIF)

- [Common API Framework (CAPIF)](#common-api-framework-capif)
- [Repository structure](#repository-structure)
- [CAPIF\_API\_Services](#capif_api_services)
  - [How to run CAPIF services in this Repository](#how-to-run-capif-services-in-this-repository)
    - [Run All CAPIF Services locally with Docker images](#run-all-capif-services-locally-with-docker-images)
    - [Run each service using Docker](#run-each-service-using-docker)
    - [Run each service using Python](#run-each-service-using-python)
- [How to test CAPIF APIs](#how-to-test-capif-apis)
  - [Test Plan Documentation](#test-plan-documentation)
  - [Robot Framework](#robot-framework)
  - [Using Curl](#using-curl)
  - [Using PostMan (only for release 1.0 of CAPIF)](#using-postman-only-for-release-10-of-capif)
- [Important urls:](#important-urls)
  - [Mongo DB Dashboard](#mongo-db-dashboard)
- [CAPIF Tool Release 1.0](#capif-tool-release-10)
- [CAPIF Tool Release 2.0](#capif-tool-release-20)
- [CAPIF Tool Release 2.1](#capif-tool-release-21)
- [CAPIF Tool Release 3.0](#capif-tool-release-30)
- [CAPIF Tool Release 3.1](#capif-tool-release-31)
- [CAPIF Tool Release 3.1.1](#capif-tool-release-311)
- [CAPIF Tool Release 3.1.2](#capif-tool-release-312)


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
[Open API Descriptions of 3GPP 5G APIs]

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

Nginx deployed by default use **capifcore** hostname, but can add a parameter when run.sh is executed setting a different hostname, for example,
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
## Test Plan Documentation

Complete documentation of tests is here: [Test Plan Directory]
## Robot Framework

In order to ensure modifications over CAPIF services still accomplish the required functionality, Robot Framework test suite must be success.

Test suite implemented accomplish requirements described under test plan at [Test Plan Directory] folder.

Please go to [Testing with Robot Framework] Section

## Using Curl

Please go to [Testing Using Curl] section.

## Using PostMan (only for release 1.0 of CAPIF)
For more information on how to test the APIs with POSTMAN, follow this [Document](docs/testing_with_postman/EVOLVED-5G%20--%20using%20CCF%20from%20Postman_13.1.2022.pdf).
Also you have here the [POSTMAN Collection](docs/testing_with_postman/CAPIF_export_APIs.postman_collection.json) **TLS NOT ADDED**

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


# CAPIF Tool Release 2.1

This CAPIF services have many stability improvements:
- API Provider Management Service adds TLS connection using certificates.
- Added logs on Services.
- Easy RSA:
  - Fix: recreate always when we try to sign a public key. Previously if there are a signed key with same filename causes a MISMATCH error.
  - Code refactor.
  - Scripts added for manual remove of signed certificates.
- JWT Auth Service:
  - code refactor
  - New register operation added, distinguish between invoker and exposer logic.
- NGINX service:
  - Adjusted rounting information.
    - TLS over API Provider Management Service.
    - removed not used endpoints
    - TLS over some endpoint at JWT Auth Service.
  - Added retry to obtain ca root certificate over Easy RSA service.
  - Added check of ca.crt obtained.
  - nginx_prepare.sh is refactored and parametrized.
- Robot Framework Test:
  - Adjusted the register flow for exposer and invoker.
  - End points used in that flow are changed.
  - API Provider Management tests adapted to use TLS.

# CAPIF Tool Release 3.0

Changes at Services:

* **Common Changes**:
  * Removed from all CAPIF services the Common Name (CN) check at certificate to get the role in services.
  * Add role verification in Nginx (check if consumer is Invoker, APF, AEF, AMF, or CCF)
  * Add log files
  * Remove mosquitto mqtt
* **NGINX service**:
  * Add map functions in config to check CN in certificates (role verification)
* **Register**:
  * Refactor
  * At Registration operation you need to setup if entity is invoker or provider (previously was invoker or exposer).
  * Get Auth operation to get access_token now only need to have user and password in body, role is not needed now.
* **Invoker**:
  * Refactor
  * Same functionality but complete code refactor performed.
  * This service has REDIS connection to update status (onboard, offboard) to other services.
  * Listener created to add apiList when security context is created and remove it when security context is destroyed.
* **Provider**:
  * Refactor
  * New development at this version.
  * Allow registration of provider entities (AMF, APF y AEF)
  * This registration returns signed certificates for each one requested to be used in subsequent request by each entity of provider.
* **Events**:
  * Refactor
  * Generate subscription to event for any entity
  * This service has REDIS connection to communicate event to other services:
    * Internal operations
      * Invoker OnBoarded or OffBoarded.
      * Other events.
    * External operations from other services.
  * Notify to subscribers
* **Publish**:
  * Refactor
  * Check if APF Id is valid.
  * This service has REDIS connection:
    * If Service is added or removed it sends a message through REDIS.
* **Security**:
  * New at this version
  * This service has REDIS connection, that allow some operations like:
  * When a new security context is created, then request to invoker to add the api to it apilist.
  * When a security list is remove those apis are removed from invoker apilist associated.
  * Token Creation (Oauth).
  * Revoke Authorizations.
* **Logging Service**:
  * New at this version
  * Creates a new log entry for service API invocations.
* **Auditing Service**
  * New at this version:
  * Query and retrieve service API invocation logs stored on the CAPIF core function.


Changes at Tests:
* **New common scenarios** in order to make easy to describe a test.
* New Test plan definition format.
* Change to new provider registration towards provider Management.
* Complete code refactor of all tests
* Complete test plan review, including all services (except auditing and logging)

# CAPIF Tool Release 3.1

* Delete a service automatically if the provider that contains the APF that published it is deleted
* Clear the security context of an invoker automatically if the invoker is deleted
* Delete automatically the entry in the security info of the security context if the provider that has the aef that published the service is deleted
* Delete automatically the entry in the security info of the security context if the service on which that context was created is deleted

# CAPIF Tool Release 3.1.1

* Minor Fixes in Logging/Auditing Service
* Update redis version

Changes at Tests:
* Add test plan to logging/auditing service
* Add tests to cover logging/auditing test plan

# CAPIF Tool Release 3.1.2

* Improvements of CAPIF robot tests.
* Update Startup scripts for all services in order to be sure service has REDIS connection and properly certificate to raise server side.

Changes at Tests:
* Allow different port for https connection.
* Improved code according to other tests to have more homogeneity when we invoke apis on all tests



[Open API Descriptions of 3GPP 5G APIs]: https://forge.3gpp.org/rep/all/5G_APIs  "Open API Descriptions of 3GPP 5G APIs"
[Test Plan Directory]: ./docs/test_plan/README.md  "Test Plan Directory"
[Testing Using Curl]: ./docs/testing_with_curl/README.md  "Testing Using Curl"
[Testing with Robot Framework]: ./docs/testing_with_robot/README.md  "Testing with Robot Framework"