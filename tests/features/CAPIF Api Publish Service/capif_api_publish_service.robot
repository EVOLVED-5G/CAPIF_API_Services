*** Settings ***
Resource        /opt/robot-tests/tests/resources/common.resource
Resource        ../../resources/common/basicRequests.robot
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

    # Sign certificate
    ${request_body}=    Sign Csr Body    ${PUBLISHER_USERNAME}    ${register_user_info['csr_request']}
    ${resp}=    Post Request Capif
    ...    sign-csr
    ...    json=${request_body}
    ...    server=${CAPIF_HTTP_URL}
    ...    verify=ca.crt
    ...    access_token=${register_user_info['access_token']}
    Status Should Be    201    ${resp}

    # Store dummy signede certificate
    Store In File    ${PUBLISHER_USERNAME}.crt    ${resp.json()['certificate']}

    # Test
    ${request_body}=    Create Service Api Description
    ${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp}

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

Retrieve all APIs Published by Authorised apfId
    [Tags]    capif_api_publish_service-3
    #Register APF
    ${register_user_info}=    Publisher Default Registration

    # Register One Service
    ${request_body}=    Create Service Api Description
    ${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp}

    # Register Other Service
    ${request_body}=    Create Service Api Description    other_service
    ${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp}

    # Retrieve Services published
    ${resp}=    Get Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    200    ${resp}

    Log List    ${resp.json()}

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

    Log List    ${resp.json()}

Retrieve single APIs Published by Authorised apfId
    [Tags]    capif_api_publish_service-5
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

    ${request_body}=    Create Service Api Description    other_service
    ${resp}=    Post Request Capif
    ...    ${register_user_info['ccf_publish_url']}
    ...    json=${request_body}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    201    ${resp}

    ${serviceApiId2}=    Set Variable    ${resp.json()['apiId']}

    # Retrieve Services 1
    ${resp}=    Get Request Capif
    ...    ${register_user_info['ccf_publish_url']}/${serviceApiId1}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    200    ${resp}

    Should Be Equal    ${resp.json()['api_name']}    first_service

    # Retrieve Services 1
    ${resp}=    Get Request Capif
    ...    ${register_user_info['ccf_publish_url']}/${serviceApiId2}
    ...    server=https://${CAPIF_HOSTNAME}/
    ...    verify=ca.crt
    ...    username=${PUBLISHER_USERNAME}

    Status Should Be    200    ${resp}

    Should Be Equal    ${resp.json()['api_name']}    other_service

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
