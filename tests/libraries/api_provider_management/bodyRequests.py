def create_api_provider_enrolment_details_body(regSec, api_prov_funcs, apiProvDomInfo="ROBOT_TESTING"):
    data = {
        "regSec": regSec,
        "apiProvFuncs": api_prov_funcs,
        "apiProvDomInfo": apiProvDomInfo,
        "suppFeat": "fffffff",
        "failReason": "string"
    }

    return (data)


def create_api_provider_function_details(username, public_key, role):
    data = {
        "regInfo": {
            "apiProvPubKey": public_key.decode("utf-8"),
        },
        "apiProvFuncRole": role,
        "apiProvFuncInfo": username

    }
    return data


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
