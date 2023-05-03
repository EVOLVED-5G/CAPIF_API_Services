*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Resource        ../../resources/common/basicRequests.robot
Resource        ../../resources/common.resource
Library         /opt/robot-tests/tests/libraries/bodyRequests.py

Test Setup      Reset Testing Environment


*** Variables ***
${APF_ID_NOT_VALID}             apf-example
${SERVICE_API_ID_NOT_VALID}     not-valid


*** Test Cases ***
Publish API by Authorised API Publisher
    [Tags]    capif_api_publish_service-1
    #Register APF
    ${register_user_info}=    Provider Default Registration

    # Test
    ${request_body}=    Create Service Api Description    service_1
    ${resp}=    Post Request Capif
    ...    /published-apis/v1/${register_user_info['apf_id']}/service-apis
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Check Response Variable Type And Values    ${resp}    201    ServiceAPIDescription
    ...    apiName=service_1
    Dictionary Should Contain Key    ${resp.json()}    apiId
    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_PUBLISH_RESOURCE_REGEX}

Publish API by NON Authorised API Publisher
    [Tags]    capif_api_publish_service-2
    #Register APF
    ${register_user_info}=    Provider Default Registration

    ${request_body}=    Create Service Api Description
    ${resp}=    Post Request Capif
    ...    /published-apis/v1/${APF_ID_NOT_VALID}/service-apis
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
    ...    status=401
    ...    title=Unauthorized
    ...    detail=Publisher not existing
    ...    cause=Publisher id not found

Retrieve all APIs Published by Authorised apfId
    [Tags]    capif_api_publish_service-3
    #Register APF
    ${register_user_info}=    Provider Default Registration

    # Register One Service
    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    service_1
    ${service_api_description_published_2}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    service_2

    # Retrieve Services published
    ${resp}=    Get Request Capif
    ...    /published-apis/v1/${register_user_info['apf_id']}/service-apis
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Check Response Variable Type And Values    ${resp}    200    ServiceAPIDescription

    List Should Contain Value    ${resp.json()}    ${service_api_description_published_1}
    List Should Contain Value    ${resp.json()}    ${service_api_description_published_2}

Retrieve all APIs Published by NON Authorised apfId
    [Tags]    capif_api_publish_service-4
    #Register APF
    ${register_user_info}=    Provider Default Registration

    # Retrieve Services published
    ${resp}=    Get Request Capif
    ...    /published-apis/v1/${APF_ID_NOT_VALID}/service-apis
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
    ...    title=Unauthorized
    ...    status=401
    ...    detail=Publisher not existing
    ...    cause=Publisher id not found

Retrieve single APIs Published by Authorised apfId
    [Tags]    capif_api_publish_service-5
    #Register APF
    ${register_user_info}=    Provider Default Registration

    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    service_1
    ${service_api_description_published_2}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    service_2

    # Store apiId1
    ${serviceApiId1}=    Set Variable    ${service_api_description_published_1['apiId']}
    ${serviceApiId2}=    Set Variable    ${service_api_description_published_2['apiId']}

    # Retrieve Services 1
    ${resp}=    Get Request Capif
    ...    /published-apis/v1/${register_user_info['apf_id']}/service-apis/${serviceApiId1}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Check Response Variable Type And Values    ${resp}    200    ServiceAPIDescription
    Dictionaries Should Be Equal    ${resp.json()}    ${service_api_description_published_1}

    # Retrieve Services 1
    ${resp}=    Get Request Capif
    ...    /published-apis/v1/${register_user_info['apf_id']}/service-apis/${serviceApiId2}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Check Response Variable Type And Values    ${resp}    200    ServiceAPIDescription
    Dictionaries Should Be Equal    ${resp.json()}    ${service_api_description_published_2}

Retrieve single APIs non Published by Authorised apfId
    [Tags]    capif_api_publish_service-6
    #Register APF
    ${register_user_info}=    Provider Default Registration

    ${resp}=    Get Request Capif
    ...    /published-apis/v1/${register_user_info['apf_id']}/service-apis/${SERVICE_API_ID_NOT_VALID}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    title=Not Found
    ...    status=404
    ...    detail=Service API not found
    ...    cause=No Service with specific credentials exists

Retrieve single APIs Published by NON Authorised apfId
    [Tags]    capif_api_publish_service-7
    # Register APF
    ${register_user_info}=    Provider Default Registration

    # Publish Service API
    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    service_1

    # Register INVOKER
    ${register_user_info_invoker}=    Invoker Default Onboarding

    ${resp}=    Get Request Capif
    ...    ${resource_url.path}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
    ...    title=Unauthorized
    ...    status=401
    ...    detail=User not authorized
    ...    cause=Certificate not authorized

Update API Published by Authorised apfId with valid serviceApiId
    [Tags]    capif_api_publish_service-8
    #Register APF
    ${register_user_info}=    Provider Default Registration

    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    service_1

    ${request_body_modified}=    Create Service Api Description    service_1_modified
    ${resp}=    Put Request Capif
    ...    ${resource_url.path}
    ...    json=${request_body_modified}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Check Response Variable Type And Values    ${resp}    200    ServiceAPIDescription
    ...    apiName=service_1_modified

    # Retrieve Service
    ${resp}=    Get Request Capif
    ...    ${resource_url.path}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Check Response Variable Type And Values    ${resp}    200    ServiceAPIDescription
    ...    apiName=service_1_modified

Update APIs Published by Authorised apfId with invalid serviceApiId
    [Tags]    capif_api_publish_service-9
    #Register APF
    ${register_user_info}=    Provider Default Registration

    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    service_1

    ${request_body}=    Create Service Api Description    service_1_modified
    ${resp}=    Put Request Capif
    ...    /published-apis/v1/${register_user_info['apf_id']}/service-apis/${SERVICE_API_ID_NOT_VALID}
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    title=Not Found
    ...    status=404
    ...    detail=Service API not existing
    ...    cause=Service API id not found

Update APIs Published by NON Authorised apfId
    [Tags]    capif_api_publish_service-10
    #Register APF
    ${register_user_info}=    Provider Default Registration

    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    service_1

    #Register INVOKER
    ${register_user_info_invoker}=    Invoker Default Onboarding

    ${request_body}=    Create Service Api Description    service_1_modified
    ${resp}=    Put Request Capif
    ...    ${resource_url.path}
    ...    json=${request_body}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
    ...    title=Unauthorized
    ...    status=401
    ...    detail=User not authorized
    ...    cause=Certificate not authorized

    # Retrieve Service
    ${resp}=    Get Request Capif
    ...    ${resource_url.path}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Check Response Variable Type And Values    ${resp}    200    ServiceAPIDescription
    ...    apiName=service_1

Delete API Published by Authorised apfId with valid serviceApiId
    [Tags]    capif_api_publish_service-11
    #Register APF
    ${register_user_info}=    Provider Default Registration

    ${service_api_description_published_1}    ${resource_url}    ${request_body}=    Publish Service Api
    ...    ${register_user_info}
    ...    first_service

    ${resp}=    Delete Request Capif
    ...    ${resource_url.path}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Status Should Be    204    ${resp}

    ${resp}=    Get Request Capif
    ...    ${resource_url.path}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    title=Not Found
    ...    status=404
    ...    detail=Service API not found
    ...    cause=No Service with specific credentials exists

Delete APIs Published by Authorised apfId with invalid serviceApiId
    [Tags]    capif_api_publish_service-12
    #Register APF
    ${register_user_info}=    Provider Default Registration

    ${resp}=    Delete Request Capif
    ...    /published-apis/v1/${register_user_info['apf_id']}/service-apis/${SERVICE_API_ID_NOT_VALID}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${APF_PROVIDER_USERNAME}

    Check Response Variable Type And Values    ${resp}    404    ProblemDetails
    ...    title=Not Found
    ...    status=404
    ...    detail=Service API not existing
    ...    cause=Service API id not found

Delete APIs Published by NON Authorised apfId
    [Tags]    capif_api_publish_service-13
    #Register APF
    ${register_user_info}=    Provider Default Registration

    #Register INVOKER
    ${register_user_info_invoker}=    Invoker Default Onboarding

    ${resp}=    Delete Request Capif
    ...    /published-apis/v1/${register_user_info['apf_id']}/service-apis/${SERVICE_API_ID_NOT_VALID}
    ...    server=${CAPIF_HTTPS_URL}
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Check Response Variable Type And Values    ${resp}    401    ProblemDetails
    ...    title=Unauthorized
    ...    status=401
    ...    detail=User not authorized
    ...    cause=Certificate not authorized
