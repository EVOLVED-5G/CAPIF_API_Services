def create_log_entry(aefId=None, apiInvokerId=None, apiId=None, apiName=None):
    data = {
    "aefId": aefId,
    "apiInvokerId": apiInvokerId,
    "logs": [
        {
        "apiId": apiId[0],
        "apiName": apiName[0],
        "apiVersion": "v1",
        "resourceName": "string",
        "uri": "http://resource/endpoint",
        "protocol": "HTTP_1_1",
        "operation": "GET",
        "result": "string",
        "invocationTime": "2023-03-30T10:30:21.408Z",
        "invocationLatency": 0,
        "inputParameters": "string",
        "outputParameters": "string",
        "srcInterface": {
            "ipv4Addr": "192.168.1.1",
            "fqdn": "string",
            "port": 65535,
            "apiPrefix": "string",
            "securityMethods": [
            "PSK",
            "string"
            ]
        },
        "destInterface": {
            "ipv4Addr": "192.168.1.23",
            "fqdn": "string",
            "port": 65535,
            "apiPrefix": "string",
            "securityMethods": [
            "PSK",
            "string"
            ]
        },
        "fwdInterface": "string"
        },
        {
        "apiId": apiId[0],
        "apiName": apiName[0],
        "apiVersion": "v2",
        "resourceName": "string",
        "uri": "http://resource/endpoint",
        "protocol": "HTTP_1_1",
        "operation": "GET",
        "result": "string",
        "invocationTime": "2023-03-30T10:30:21.408Z",
        "invocationLatency": 0,
        "inputParameters": "string",
        "outputParameters": "string",
        "srcInterface": {
            "ipv4Addr": "192.168.1.1",
            "fqdn": "string",
            "port": 65535,
            "apiPrefix": "string",
            "securityMethods": [
            "PSK",
            "string"
            ]
        },
        "destInterface": {
            "ipv4Addr": "192.168.1.23",
            "fqdn": "string",
            "port": 65535,
            "apiPrefix": "string",
            "securityMethods": [
            "PSK",
            "string"
            ]
        },
        "fwdInterface": "string"
        }
    ],
    "supportedFeatures": "ffff"
    }
    return data 

def create_log_entry_bad_service(aefId=None, apiInvokerId=None):
    data = {
    "aefId": aefId,
    "apiInvokerId": apiInvokerId,
    "logs": [
        {
        "apiId": "not-exist",
        "apiName": "not-exist",
        "apiVersion": "string",
        "resourceName": "string",
        "uri": "string",
        "protocol": "HTTP_1_1",
        "operation": "GET",
        "result": "string",
        "invocationTime": "2023-03-30T10:30:21.408Z",
        "invocationLatency": 0,
        "inputParameters": "string",
        "outputParameters": "string",
        "srcInterface": {
            "ipv4Addr": "192.168.1.1",
            "fqdn": "string",
            "port": 65535,
            "apiPrefix": "string",
            "securityMethods": [
            "PSK",
            "string"
            ]
        },
        "destInterface": {
            "ipv4Addr": "192.168.1.23",
            "fqdn": "string",
            "port": 65535,
            "apiPrefix": "string",
            "securityMethods": [
            "PSK",
            "string"
            ]
        },
        "fwdInterface": "string"
        }
    ],
    "supportedFeatures": "ffff"
    }
    return data 

def get_api_ids_and_names_from_discover_response(discover_response):
    api_ids=[]
    api_names=[]
    service_api_descriptions = discover_response.json()['serviceAPIDescriptions']
    for service_api_description in service_api_descriptions:
        api_ids.append(service_api_description['apiId'])
        api_names.append(service_api_description['apiName'])
    return api_ids, api_names
