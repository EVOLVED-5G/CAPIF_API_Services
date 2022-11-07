def create_api_provider_enrolment_details_body(apiProvDomInfo="ROBOT_TESTING"):
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
        "apiProvDomInfo": apiProvDomInfo,
        "suppFeat": "fffffff",
        "failReason": "string"
    }

    return (data)

def create_api_provider_enrolment_details_patch_body(apiProvDomInfo="ROBOT_TESTING"):
    data = {
        "apiProvFuncs": [
            {
                "apiProvFuncId": "PATCH",
                "regInfo": {
                    "apiProvPubKey": "PATCH",
                    "apiProvCert": "PATCH"
                },
                "apiProvFuncRole": "AEF",
                "apiProvFuncInfo": "PATCH"
            }
        ],
        "apiProvDomInfo": apiProvDomInfo,
    }

    return (data)
