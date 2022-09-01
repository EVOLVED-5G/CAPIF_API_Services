def create_api_provider_enrolment_details_body():
    data = {
        "regSec": "string",
        "apiProvFuncs": [
            {
                "apiProvFuncId": "string",
                "regInfo": {
                    "apiProvPubKey": "string",
                    "apiProvCert": "string"
                },
                "apiProvFuncRole": "AEF",
                "apiProvFuncInfo": "string"
            }
        ],
        "apiProvDomInfo": "ROBOT_TESTING",
        "suppFeat": "fffffff",
        "failReason": "string"
    }

    return (data)
