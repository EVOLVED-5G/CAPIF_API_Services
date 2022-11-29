def create_service_security_body(notificationDestination='http://robot.testing', aef_id=None):
    data = {
        "notificationDestination": notificationDestination,
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


def create_access_token_req_body():
    return {
        "client_id": "client_id",
        "client_secret": "client_secret",
        "grant_type": "client_credentials",
        "scope": "scope"
    }
