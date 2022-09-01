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

def create_api_provider_enrolment_details_patch_body():
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
        "apiProvDomInfo": "ROBOT_TESTING",
    }

    return (data)
