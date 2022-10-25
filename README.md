# Common API Framework (CAPIF)

- [Common API Framework (CAPIF)](#common-api-framework-capif)
- [Repository structure](#repository-structure)
- [CAPIF_API_Services](#capif_api_services)
  - [How to run CAPIF services in this Repository](#how-to-run-capif-services-in-this-repository)
    - [Run All CAPIF Services locally with Docker images](#run-all-capif-services-locally-with-docker-images)
    - [Run each service using Docker](#run-each-service-using-docker)
    - [Run each service using Python](#run-each-service-using-python)
- [How to test CAPIF APIs](#how-to-test-capif-apis)
  - [Robot Framework](#robot-framework)
    - [Test Plan Documentation](#test-plan-documentation)
      - [Execution](#execution)
        - [Script Test Execution](#script-test-execution)
        - [Manual Build And Test Execution](#manual-build-and-test-execution)
    - [Test result review](#test-result-review)
  - [Using Curl](#using-curl)
  - [Using PostMan (only for release 1.0 of CAPIF)](#using-postman-only-for-release-10-of-capif)
- [Important urls:](#important-urls)
  - [Mongo DB Dashboard](#mongo-db-dashboard)
- [CAPIF Tool Release 1.0](#capif-tool-release-10)
- [CAPIF Tool Release 2.0](#capif-tool-release-20)
- [CAPIF Tool Release 2.1](#capif-tool-release-21)


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
## Robot Framework

In order to ensure modifications over CAPIF services still accomplish the required functionality, Robot Framework test suite must be success.

Test suite implemented accomplish requirements described under test plan at [Test Plan Directory] folder.
### Test Plan Documentation

Complete documentation of tests is here: [Test Plan Directory]

#### Execution
**Previously Steps**
To run any test locally you will need docker and docker-compose installed in order run services and execute test plan. Steps will be:
* **Run All Services**: See section [Run All CAPIF Services](#run-all-capif-services-locally-with-docker-images)
* **Run desired tests**: At this point we have 2 options:
  * **Using helper script**: [Script Test Execution](#script-test-execution)
  * **Build robot docker image and execute manually robot docker**: [Manual Build And Test Execution](#manual-build-and-test-execution)


##### Script Test Execution
This script will build robot docker image if it's need and execute tests selected by "include" option. Just go to service folder, execute and follow steps.
```
./runCapifTests.sh --include <TAG>
```
Results will be stored at <REPOSITORY_FOLDER>/results

Please check parameters (include) under *Test Execution* under [Manual Build And Test Execution](#manual-build-and-test-execution).

##### Manual Build And Test Execution

* **Build Robot docker image**:
```
cd tools/robot
docker build . -t 5gnow-robot-test:latest
```

* **Tests Execution**:
  
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



[Open API Descriptions of 3GPP 5G APIs]: https://github.com/jdegre/5GC_APIs  "Open API Descriptions of 3GPP 5G APIs"
[Test Plan Directory]: ./docs/test_plan/README.md  "Test Plan Directory"
[Testing Using Curl]: ./docs/testing_with_curl/README.md  "Testing Using Curl"