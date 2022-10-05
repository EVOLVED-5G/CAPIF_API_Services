
from capif_security.models import ServiceSecurity


json_data = {
    "securityInfo": [
      {
        "interfaceDetails": {
          "ipv4Addr": "string",
          "ipv6Addr": "string",
          "port": 65535,
          "securityMethods": [
            "PSK",
            "PKI"
          ]
        },
        "aefId": "string",
        "apiId": "string",
        "prefSecurityMethods": [
          "PSK",
          "PKI"
        ],
        "selSecurityMethod": "PSK",
        "authenticationInfo": "string",
        "authorizationInfo": "string"
      },
      {
        "interfaceDetails": {
          "ipv4Addr": "string",
          "ipv6Addr": "string",
          "port": 65535,
          "securityMethods": [
            "PSK",
            "string"
          ]
        },
        "aefId": "string",
        "apiId": "string",
        "prefSecurityMethods": [
          "PSK",
          "string"
        ],
        "selSecurityMethod": "PSK",
        "authenticationInfo": "string",
        "authorizationInfo": "string"
      }
    ],
    "notificationDestination": "string",
    "requestTestNotification": True,
    "websockNotifConfig": {
      "websocketUri": "string",
      "requestWebsocketUri": True
    },
    "supportedFeatures": "fff"
  }

#print(json_data)

my_ser = ServiceSecurity.from_dict(json_data)

print(my_ser)