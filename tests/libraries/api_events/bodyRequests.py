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
            "partitionCriteria": ["string1", "string2"],
            "repPeriod": 6,
            "sampRatio": 15
        },
        "events": ["event_name_id_1", "event_name_id_2"],
        "notificationDestination": "ROBOT_TESTING",
        "requestTestNotification": True,
        "supportedFeatures": "aaa",
        "websockNotifConfig": {
            "requestWebsocketUri": True,
            "websocketUri": "websocketUri"
        }
    }
