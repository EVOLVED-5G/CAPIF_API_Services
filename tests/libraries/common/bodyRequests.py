from operator import contains


def sign_csr_body(username, public_key):
    data = {
        "csr":  public_key.decode("utf-8"),
        "mode":  "client",
        "filename": username
    }
    return data


def check_duplicates(input_list):
    return any(input_list.count(element) > 1 for element in input_list)


def check_attributes(body, mandatory_attributes, optional_parameters):
    # Check is mandatory and optional parameters are not duplicated
    if check_duplicates(mandatory_attributes):
        print("WARNING.Mandatory attributes contains duplicated keys")
        mandatory_attributes = list(dict.fromkeys(mandatory_attributes))
    if check_duplicates(optional_parameters):
        print("WARNING.Optional attributes contains duplicated keys")
        optional_parameters = list(dict.fromkeys(optional_parameters))

    all_attributes = mandatory_attributes + optional_parameters
    if check_duplicates(all_attributes):
        raise Exception('Duplicated keys between mandatory and optional keys.')

    # Check if body has not allowed attributes
    print(body.keys())
    for body_key in body.keys():
        if body_key not in all_attributes:
            raise Exception('Attribute "' + body_key +
                            '" is not present as a mandatory or optional key (' + ','.join(all_attributes) + ')')

    for mandatory_key in mandatory_attributes:
        if mandatory_key not in body.keys():
            raise Exception('Mandatory Attribute "' + mandatory_key +
                            '" is not present at body under check')


def check_invalid_params(input):
    mandatory_attributes = ["param"]
    optional_parameters = ["reason"]
    for invalid_param in input:
        check_attributes(invalid_param, mandatory_attributes,
                         optional_parameters)


def check_problem_details_schema(input):
    mandatory_attributes = []
    optional_parameters = ["type", "title", "status", "detail",
                           "instance", "cause", "invalidParams", "supportedFeatures"]
    check_attributes(input, mandatory_attributes, optional_parameters)
    if "invalidParams" in input.keys():
        check_invalid_params(input["invalidParams"])


def check_onboarding_information(input):
    mandatory_attributes = ["apiInvokerPublicKey"]
    optional_parameters = ["apiInvokerCertificate","onboardingSecret"]
    check_attributes(input, mandatory_attributes, optional_parameters)

def check_websock_notif_config(input):
    mandatory_attributes = []
    optional_parameters = ["websocketUri","requestWebsocketUri"]
    check_attributes(input, mandatory_attributes, optional_parameters)

def check_api_list(input):
    for api in input:
        check_service_api_description(api)

def check_service_api_description(input):
    # This check is not complete, just minimun check of mandatory and optional attributes
    mandatory_attributes = ["apiName","apiId"]
    optional_parameters = ["aefProfiles","description","supportedFeatures","shareableInfo","serviceAPICategory","apiSuppFeats","pubApiPath","ccfId"]
    check_attributes(input, mandatory_attributes, optional_parameters)

def check_api_invoker_enrolment_details_response(input):
    #no value check for suupportedFeatures or value type
    mandatory_attributes = ["onboardingInformation",
                            "notificationDestination", "apiInvokerId"]
    optional_parameters = ["requestTestNotification", "websockNotifConfig",
                           "apiList", "apiInvokerInformation", "supportedFeatures"]
    check_attributes(input, mandatory_attributes, optional_parameters)
    
    # Check Mandatory attributes
    check_onboarding_information(input['onboardingInformation'])
    #Check Optional attributes    
    if "websockNotifConfig" in input.keys():
        check_websock_notif_config(input["websockNotifConfig"])
    if "apiList" in input.keys():
        check_service_api_description



# def example_problem_detail():
#     problem_detail= {
#         "type": "string",
#         "title": "string",
#         "status": 0,
#         "detail": "string",
#         "instance": "string",
#         "cause": "string",
#         "invalidParams": [
#             {
#             "param": "string",
#             "reason": "string"
#             }
#         ],
#         "supportedFeatures": "string"
#         }
#     return problem_detail

# def example2_problem_detail():
#     problem_detail= {
#         "pepito": "pepito",
#         "type": "string",
#         "title": "string",
#         "status": 0,
#         "detail": "string",
#         "instance": "string",
#         "cause": "string",
#         "invalidParams": [
#             {
#             "param": "string",
#             "reason": "string"
#             }
#         ],
#         "supportedFeatures": "string"
#         }
#     return problem_detail
