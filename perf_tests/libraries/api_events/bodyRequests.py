def create_events_subscription():
    return {
        "eventFilters": [
            {
                "aefIds": ["aefIds", "aefIds"],
                "apiIds": ["apiIds", "apiIds"],
                "apiInvokerIds": ["apiInvokerIds", "apiInvokerIds"]
            },
            {
                "aefIds": ["aefIds", "aefIds"],
                "apiIds": ["apiIds", "apiIds"],
                "apiInvokerIds": ["apiInvokerIds", "apiInvokerIds"]
            }
        ],
        "eventReq": {
            "grpRepTime": 5,
            "immRep": True,
            "maxReportNbr": 0,
            "monDur": "2000-01-23T04:56:07+00:00",
            "partitionCriteria": ["TAC", "GEOAREA"],
            "repPeriod": 6,
            "sampRatio": 15
        },
        "events": ["SERVICE_API_AVAILABLE", "API_INVOKER_ONBOARDED"],
        "notificationDestination": "http://robot.testing",
        "requestTestNotification": True,
        "supportedFeatures": "aaa",
        "websockNotifConfig": {
            "requestWebsocketUri": True,
            "websocketUri": "websocketUri"
        }
    }
