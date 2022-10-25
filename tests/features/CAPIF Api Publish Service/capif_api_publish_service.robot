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
    ${register_user_info}=    Register User At Jwt Auth
    ...    username=${PUBLISHER_USERNAME}    role=${PUBLISHER_ROLE}

    # Test
    ${request_body}=    Create Service Api Description
    ${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp}
    Check Variable    ${resp.json()}    ServiceAPIDescription
    Dictionary Should Contain Key    ${resp.json()}    apiId
    ${resource_url}=    Check Location Header    ${resp}    ${LOCATION_PUBLISH_RESOURCE_REGEX}

Publish API by NON Authorised API Publisher
    [Tags]    capif_api_publish_service-2
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    ${request_body}=    Create Service Api Description
    ${resp}=    Post Request Capif
    ...    /published-apis/v1/${APF_ID_NOT_VALID}/service-apis
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    401    ${resp}
    Check Problem Details
    ...    ${resp}
    ...    title=Unauthorized
    ...    status=401
    ...    detail=Exposer not existing
    ...    cause=Exposer id not found

Retrieve all APIs Published by Authorised apfId
    [Tags]    capif_api_publish_service-3
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    # Register One Service
    ${request_body}=    Create Service Api Description    service_1
    ${resp_service_1}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp_service_1}
    Check Variable    ${resp_service_1.json()}    ServiceAPIDescription
    Dictionary Should Contain Key    ${resp_service_1.json()}    apiId
    ${resource_url}=    Check Location Header    ${resp_service_1}    ${LOCATION_PUBLISH_RESOURCE_REGEX}

    # Register Other Service
    ${request_body}=    Create Service Api Description    service_2
    ${resp_service_2}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp_service_2}
    Check Variable    ${resp_service_2.json()}    ServiceAPIDescription
    Dictionary Should Contain Key    ${resp_service_2.json()}    apiId
    ${resource_url}=    Check Location Header    ${resp_service_2}    ${LOCATION_PUBLISH_RESOURCE_REGEX}

    # Retrieve Services published
    ${resp}=    Get Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    200    ${resp}
    Check Variable    ${resp.json()}    ServiceAPIDescription

    Log List    ${resp.json()}

    List Should Contain Value    ${resp.json()}    ${resp_service_1.json()}
    List Should Contain Value    ${resp.json()}    ${resp_service_2.json()}

Retrieve all APIs Published by NON Authorised apfId
    [Tags]    capif_api_publish_service-4
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    # Retrieve Services published
    ${resp}=    Get Request Capif
    ...    /published-apis/v1/${APF_ID_NOT_VALID}/service-apis
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    401    ${resp}
    Check Problem Details
    ...    ${resp}
    ...    title=Unauthorized
    ...    status=401
    ...    detail=Exposer not existing
    ...    cause=Exposer id not found

Retrieve single APIs Published by Authorised apfId
    [Tags]    capif_api_publish_service-5
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    ${request_body}=    Create Service Api Description    service_1
    ${resp_service_1}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp_service_1}
    Check Variable    ${resp_service_1.json()}    ServiceAPIDescription
    Dictionary Should Contain Key    ${resp_service_1.json()}    apiId
    ${resource_url}=    Check Location Header    ${resp_service_1}    ${LOCATION_PUBLISH_RESOURCE_REGEX}

    # Store apiId1
    ${serviceApiId1}=    Set Variable    ${resp_service_1.json()['apiId']}

    ${request_body}=    Create Service Api Description    service_2
    ${resp_service_2}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp_service_2}
    Check Variable    ${resp_service_2.json()}    ServiceAPIDescription
    Dictionary Should Contain Key    ${resp_service_2.json()}    apiId
    ${resource_url}=    Check Location Header    ${resp_service_2}    ${LOCATION_PUBLISH_RESOURCE_REGEX}

    # Store apiId2
    ${serviceApiId2}=    Set Variable    ${resp_service_2.json()['apiId']}

    # Retrieve Services 1
    ${resp}=    Get Request Capif
    ...    ${register_user_info['ccf_publish_url']}/${serviceApiId1}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    200    ${resp}
    Check Variable    ${resp.json()}    ServiceAPIDescription
    Dictionaries Should Be Equal  ${resp.json()}    ${resp_service_1.json()}

    # Retrieve Services 1
    ${resp}=    Get Request Capif
    ...    ${register_user_info['ccf_publish_url']}/${serviceApiId2}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    200    ${resp}
    Check Variable    ${resp.json()}    ServiceAPIDescription
    Dictionaries Should Be Equal  ${resp.json()}    ${resp_service_2.json()}

Retrieve single APIs non Published by Authorised apfId
    [Tags]    capif_api_publish_service-6
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    ${resp}=    Get Request Capif
    ...    ${register_user_info['ccf_publish_url']}/${SERVICE_API_ID_NOT_VALID}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    404    ${resp}

    Log    ${resp.json()}

Retrieve single APIs Published by NON Authorised apfId
    [Tags]    capif_api_publish_service-7
    # [Setup]    Initialize Test And Register    role=invoker
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    #Register INVOKER
    ${register_user_info_invoker}=    Invoker Default Onboarding

    ${resp}=    Get Request Capif
    ...    ${register_user_info['ccf_publish_url']}/${SERVICE_API_ID_NOT_VALID}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    401    ${resp}

    Log    ${resp.json()}

Update API Published by Authorised apfId with valid serviceApiId
    [Tags]    capif_api_publish_service-8
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    ${request_body}=    Create Service Api Description    first_service
    ${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp}

    ${serviceApiId1}=    Set Variable    ${resp.json()['apiId']}
    ${url}=    Parse Url    ${resp.headers['Location']}

    ${request_body}=    Create Service Api Description    first_service_modified
    ${resp}=    Put Request Capif
    ...    ${url.path}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    200    ${resp}

Update APIs Published by Authorised apfId with invalid serviceApiId
    [Tags]    capif_api_publish_service-9
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    ${request_body}=    Create Service Api Description    first_service_modified
    ${resp}=    Put Request Capif
    ...    ${register_user_info['ccf_publish_url']}/${SERVICE_API_ID_NOT_VALID}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    404    ${resp}

Update APIs Published by NON Authorised apfId
    [Tags]    capif_api_publish_service-10
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    ${request_body}=    Create Service Api Description    first_service
    ${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp}

    ${serviceApiId1}=    Set Variable    ${resp.json()['apiId']}
    ${url}=    Parse Url    ${resp.headers['Location']}

    #Register INVOKER
    ${register_user_info_invoker}=    Invoker Default Onboarding

    ${request_body}=    Create Service Api Description    first_service_modified
    ${resp}=    Put Request Capif
    ...    ${url.path}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    401    ${resp}

Delete API Published by Authorised apfId with valid serviceApiId
    [Tags]    capif_api_publish_service-11
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    ${request_body}=    Create Service Api Description    first_service
    ${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp}

    ${serviceApiId1}=    Set Variable    ${resp.json()['apiId']}
    ${url}=    Parse Url    ${resp.headers['Location']}

    ${resp}=    Delete Request Capif
    ...    ${url.path}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    204    ${resp}

Delete APIs Published by Authorised apfId with invalid serviceApiId
    [Tags]    capif_api_publish_service-12
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    ${resp}=    Delete Request Capif
    ...    ${register_user_info['ccf_publish_url']}/${SERVICE_API_ID_NOT_VALID}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    404    ${resp}

Delete APIs Published by NON Authorised apfId
    [Tags]    capif_api_publish_service-13
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    #Register INVOKER
    ${register_user_info_invoker}=    Invoker Default Onboarding

    ${resp}=    Delete Request Capif
    ...    ${register_user_info['ccf_publish_url']}/${SERVICE_API_ID_NOT_VALID}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${INVOKER_USERNAME}

    Status Should Be    401    ${resp}
