def create_service_security_body(notificationDestination='http://robot.testing'):
    return {
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
        },
            {
            "authenticationInfo": "authenticationInfo",
            "authorizationInfo": "authorizationInfo",
            "prefSecurityMethods": ["PSK", "PKI", "OAUTH"],
            "aefId": "aefId"
        }],
        "websockNotifConfig": {
            "requestWebsocketUri": True,
            "websocketUri": "websocketUri"
        },
        "requestTestNotification": True
    }


def create_security_notification_body(api_invoker_id):
    # cause must be one of [ OVERLIMIT_USAGE, UNEXPECTED_REASON ]
    return {
        "aefId": "aefId",
        "apiIds": [
            "apiIds",
            "apiIds"
        ],
        "apiInvokerId": api_invoker_id,
        "cause": "OVERLIMIT_USAGE"
    }


def create_access_token_req_body():
    return {
        "client_id": "client_id",
        "client_secret": "client_secret",
        "grant_type": "client_credentials",
        "scope": "scope"
    }
