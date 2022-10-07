from operator import contains
import re
import json
from xmlrpc.client import boolean

f = open('/opt/robot-tests/tests/libraries/common/types.json')
capif_types = json.load(f)


def check_jms():
    err = prob_example()
    check_variable(err, "ProblemDetails")


def check_variable(input, data_type):
    print(input)
    print(data_type)
    if isinstance(input, list):
        for one in input:
            check_variable(one, data_type)
            return True
    if data_type == "string":
        if isinstance(input, str):
            return True
        else:
            raise Exception("variable is not string type")
    elif data_type == "integer":
        if isinstance(input, int):
            return True
        else:
            raise Exception("variable is not integer type")
    elif data_type == "boolean":
        if isinstance(input, boolean):
            return True
        else:
            raise Exception("variable is not integer type")
    elif data_type == "SupportedFeatures":
        check_supported_features(input)
        return True
    elif data_type not in capif_types.keys():
        raise Exception("ERROR, type " + data_type +
                        " is not present in types file")
    if "Check" in capif_types[data_type].keys():
        if not capif_types[data_type]["Check"]:
            return True
    if "enum" in capif_types[data_type].keys():
        if input in capif_types[data_type]["enum"]:
            print("value (" + input + ") is present at enum (" +
                  ','.join(capif_types[data_type]["enum"]) + ")")
            return True
        else:
            raise Exception("value (" + input + ") is not present at enum (" +
                            ','.join(capif_types[data_type]["enum"]) + ")")
    # Check Structure
    all_attributes = check_attributes_dict(input, data_type)

    print('Check Variable type')
    # Check Variable type
    for key in input.keys():
        print(key)
        check_variable(input[key], all_attributes[key])


def check_attributes_dict(body, data_type):
    mandatory_attributes = capif_types[data_type]["mandatory_attributes"]
    optional_parameters = capif_types[data_type]["optional_attributes"]
    all_attributes = mandatory_attributes | optional_parameters
    # Check if body has not allowed attributes

    for body_key in body.keys():
        if body_key not in all_attributes.keys():
            raise Exception('Attribute "' + body_key +
                            '" is not present as a mandatory or optional key (' + ','.join(all_attributes.keys()) + ')')

    if mandatory_attributes:
        for mandatory_key in mandatory_attributes.keys():
            if mandatory_key not in body.keys():
                raise Exception('Mandatory Attribute "' + mandatory_key +
                                '" is not present at body under check')
    return all_attributes


# def prob_example():
#     return {
#         "type": "string",
#         "title": "string",
#         "status": "string",
#         "detail": "string",
#         "instance": "string",
#         "cause": "string",
#         "invalidParams": [
#             {
#                 "param": "string",
#                 "reason": "string"
#             }
#         ],
#         "supportedFeatures": "fffffff"
#     }


def sign_csr_body(username, public_key):
    data = {
        "csr":  public_key.decode("utf-8"),
        "mode":  "client",
        "filename": username
    }
    return data


# def check_duplicates(input_list):
#     return any(input_list.count(element) > 1 for element in input_list)


# def check_attributes(body, mandatory_attributes, optional_parameters):
#     # Check is mandatory and optional parameters are not duplicated
#     if check_duplicates(mandatory_attributes):
#         print("WARNING.Mandatory attributes contains duplicated keys")
#         mandatory_attributes = list(dict.fromkeys(mandatory_attributes))
#     if check_duplicates(optional_parameters):
#         print("WARNING.Optional attributes contains duplicated keys")
#         optional_parameters = list(dict.fromkeys(optional_parameters))

#     all_attributes = mandatory_attributes + optional_parameters
#     if check_duplicates(all_attributes):
#         raise Exception('Duplicated keys between mandatory and optional keys.')

#     # Check if body has not allowed attributes
#     print(body.keys())
#     for body_key in body.keys():
#         if body_key not in all_attributes:
#             raise Exception('Attribute "' + body_key +
#                             '" is not present as a mandatory or optional key (' + ','.join(all_attributes) + ')')

#     for mandatory_key in mandatory_attributes:
#         if mandatory_key not in body.keys():
#             raise Exception('Mandatory Attribute "' + mandatory_key +
#                             '" is not present at body under check')


def check_supported_features(input):
    matched = re.match("^[A-Fa-f0-9]*$", input)
    is_match = bool(matched)
    if is_match:
        print("Valid Supported Features")
    else:
        raise Exception("Supported Features(" + input + ") is not valid.")


# def check_invalid_params(input):
#     mandatory_attributes = ["param"]
#     optional_parameters = ["reason"]
#     for invalid_param in input:
#         check_attributes(invalid_param, mandatory_attributes,
#                          optional_parameters)


# def check_problem_details_schema(input):
#     mandatory_attributes = []
#     optional_parameters = ["type", "title", "status", "detail",
#                            "instance", "cause", "invalidParams", "supportedFeatures"]
#     check_attributes(input, mandatory_attributes, optional_parameters)

#     # Check Optional attributes
#     if "invalidParams" in input.keys():
#         check_invalid_params(input["invalidParams"])
#     if "supportedFeatures" in input.keys():
#         check_supported_features(input["supportedFeatures"])


# def check_onboarding_information(input):
#     mandatory_attributes = ["apiInvokerPublicKey"]
#     optional_parameters = ["apiInvokerCertificate", "onboardingSecret"]
#     check_attributes(input, mandatory_attributes, optional_parameters)


# def check_websock_notif_config(input):
#     mandatory_attributes = []
#     optional_parameters = ["websocketUri", "requestWebsocketUri"]
#     check_attributes(input, mandatory_attributes, optional_parameters)


# def check_aef_profile(input):
#     mandatory_attributes = ["aefId", "versions"]
#     optional_parameters = ["protocol", "dataFormat", "securityMethods",
#                            "domainName", "interfaceDescriptions", "aefLocation"]
#     check_attributes(input, mandatory_attributes, optional_parameters)

#     for version in input["versions"]:
#         check_version(version)


# def check_version(input):
#     mandatory_attributes = ["apiVersion"]
#     optional_parameters = ["expiry", "resources", "custOperations"]
#     check_attributes(input, mandatory_attributes, optional_parameters)
#     # TODO: resources and custOperations checks


# def check_service_api_description(input):
#     # This check is not complete, just minimun check of mandatory and optional attributes
#     mandatory_attributes = ["apiName", "apiId"]
#     optional_parameters = ["aefProfiles", "description", "supportedFeatures",
#                            "shareableInfo", "serviceAPICategory", "apiSuppFeats", "pubApiPath", "ccfId"]
#     check_attributes(input, mandatory_attributes, optional_parameters)

#     if "aefProfiles" in input.keys():
#         for aef_profile in input["aefProfiles"]:
#             check_aef_profile(aef_profile)


# def check_api_invoker_enrolment_details_response(input):
#     mandatory_attributes = ["onboardingInformation",
#                             "notificationDestination", "apiInvokerId"]
#     optional_parameters = ["requestTestNotification", "websockNotifConfig",
#                            "apiList", "apiInvokerInformation", "supportedFeatures"]
#     check_attributes(input, mandatory_attributes, optional_parameters)

#     # Check Mandatory attributes
#     check_onboarding_information(input['onboardingInformation'])
#     # Check Optional attributes
#     if "websockNotifConfig" in input.keys():
#         check_websock_notif_config(input["websockNotifConfig"])
#     if "apiList" in input.keys():
#         for api in input["apiList"]:
#             check_service_api_description(api)
#     if "supportedFeatures" in input.keys():
#         check_supported_features(input["supportedFeatures"])
