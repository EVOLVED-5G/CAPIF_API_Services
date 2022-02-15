def create_service_security_body():
    return {
        "notificationDestination": "ROBOT_TESTING",
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
