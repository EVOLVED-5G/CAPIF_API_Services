# CAPIF_API_Services
This repository has the python-flask Mockup servers created with openapi-generator related with CAPIF APIS defined here:
https://github.com/jdegre/5GC_APIs

# How to run CAPIF services in this Repository

## Run All CAPIF Services locally with Docker images

To run using docker and docker-compose you must ensure you have that tools installed at your machine. Also to simplify the process, we have 3 script to control docker images to deploy, check and cleanup.

To run all CAPIF APIs locally using docker and docker-compose you can execute:
```
./run.sh
```
This will build and run all services using docker images, including mongodb and nginx locally and in background.

If you want to check if all CAPIF services are running properly in local machine after execute run.sh, we can use:
```
check_services_are_running.sh
```
This shell script will return 0 if all services are running properly.

When we need to stop CAPIF services, we can use next bash script:
```
clean_capif_docker_services.sh
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


# Test Plan Documentation

[Test Plan Directory](./docs/test_plan/README.md)


Additional info:
```
post_body_example.json:
Example of APIInvokerEnrolmentDetails object for POST request of API_Invoker_Management API 


Mongo Express url:
http://0.0.0.0:8081/
```

