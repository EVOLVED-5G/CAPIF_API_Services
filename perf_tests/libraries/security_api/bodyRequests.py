def create_service_security_body(notification_destination, aef_id=None):
    data = {
        "notificationDestination": notification_destination,
        "supportedFeatures": "fffffff",
        "securityInfo": [{
            "authenticationInfo": "authenticationInfo",
            "authorizationInfo": "authorizationInfo",
            "interfaceDetails": {
                "ipv4Addr": "127.0.0.1",
                "securityMethods": ["PSK"],
                "port": 5248
            },
            "prefSecurityMethods": ["PSK", "PKI", "OAUTH"],
        }
        ],
        "websockNotifConfig": {
            "requestWebsocketUri": True,
            "websocketUri": "websocketUri"
        },
        "requestTestNotification": True
    }

    if aef_id != None:
        data['securityInfo'].append({
            "authenticationInfo": "authenticationInfo",
            "authorizationInfo": "authorizationInfo",
            "prefSecurityMethods": ["PSK", "PKI", "OAUTH"],
            "aefId": aef_id
        })

    return data


def create_service_security_from_discover_response(notification_destination, discover_response):
    data = {
        "notificationDestination": notification_destination,
        "supportedFeatures": "fffffff",
        "securityInfo": [],
        "websockNotifConfig": {
            "requestWebsocketUri": True,
            "websocketUri": "websocketUri"
        },
        "requestTestNotification": True
    }
    service_api_descriptions = discover_response.json()['serviceAPIDescriptions']
    for service_api_description in service_api_descriptions:
        for aef_profile in service_api_description['aefProfiles']:
            data['securityInfo'].append({
                "authenticationInfo": "authenticationInfo",
                "authorizationInfo": "authorizationInfo",
                "prefSecurityMethods": ["PSK", "PKI", "OAUTH"],
                "aefId": aef_profile['aefId'],
                "apiId": service_api_description['apiId']
            })
    return data


def create_security_notification_body(api_invoker_id, api_ids, cause="OVERLIMIT_USAGE", aef_id=None):
    # cause must be one of [ OVERLIMIT_USAGE, UNEXPECTED_REASON ]
    data = {
        "apiIds": api_ids,
        "apiInvokerId": api_invoker_id,
        "cause": cause
    }

    if isinstance(api_ids,list):
        data['apiIds'] = api_ids
    else:
        data['apiIds'] = [ api_ids ]

    if aef_id != None:
        data['aefId'] = aef_id
    

    return data


def create_access_token_req_body(client_id, scope, client_secret=None,grant_type="client_credentials"):
    data = {
        "client_id": client_id,
        "grant_type": grant_type,
        "scope": scope
    }

    if client_secret != None:
        data['client_secret'] = client_secret

    return data

def get_api_ids_from_discover_response(discover_response):
    api_ids=[]
    service_api_descriptions = discover_response.json()['serviceAPIDescriptions']
    for service_api_description in service_api_descriptions:
        api_ids.append(service_api_description['apiId'])
    return api_ids
