def create_onboarding_notification_body(notification_destination="https://host.docker.internal/netapp_callback", api_invoker_public_key="ApiInvokerPublicKey",api_invoker_information='ROBOT_TESTING', api_invoker_id=None):
    data = {
        "notificationDestination": notification_destination,
        "supportedFeatures": "fffffff",
        "apiInvokerInformation": api_invoker_information,
        "websockNotifConfig": {
            "requestWebsocketUri": True,
            "websocketUri": "websocketUri"
        },
        "onboardingInformation": {
            "apiInvokerPublicKey": api_invoker_public_key.decode("utf-8"),
            "onboardingSecret": "onboardingSecret",
            "apiInvokerCertificate": "apiInvokerCertificate"
        },
        "requestTestNotification": True
    }
    if api_invoker_id != None:
        data['apiInvokerId'] = api_invoker_id

    return (data)
