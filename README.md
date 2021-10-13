# CAPIF_API_Services
This repository has the python-flask Mockup servers created with openapi-generator related with CAPIF APIS defined here:
https://github.com/jdegre/5GC_APIs

To run using docker and docker-compose you must ensure you have that tools installed at your machine.

To run all CAPIF APIs at same time you can execute:
```
./run.sh
```

Also you can run service by service using docker:
```
cd <Service>
docker build -t openapi_server .
docker run -p 8080:8080 openapi_server
```

Or directly python
```
cd <Service>
pip3 install -r requirements.txt
python3 -m <service>
```

Additional info:
```
post_body_example.json:
Example of APIInvokerEnrolmentDetails object for POST request of API_Invoker_Management API 


Mongo Express url:
http://0.0.0.0:8081/
```
