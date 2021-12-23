*** Settings ***
Library     /opt/robot-tests/tests/libraries/helpers.py
Resource    /opt/robot-tests/common/customKeywords/utils.robot
Library     MongoDBLibrary

*** Variables ***
${MONGO_URL}    http://localhost:27017

*** Keywords ***
Initialize Test And Register
	[Arguments]    ${password}=password    ${username}=robot    ${role}=invoker    ${description}=Testing    ${db_col}=

    Reset Db                     ${db_col}
    Register User At Jwt Auth    password=${password}    username=${username}    role=${role}    description=${description}

Reset Db
	[Arguments]    ${db_col}
	Log            Db capif.invokerdetails collection will be removed in order to isolate each test.

	${host}    ${port}=    Get Db Host    ${MONGO_URL}

	Connect To MongoDB    mongodb://root:example@${host}	${port}

	@{allCollections}=            Get MongoDB Collections    capif
	Log Many	@{allCollections}

	Run Keyword And Ignore Error   Drop MongoDB Collection    capif    invokerdetails
	Run Keyword And Ignore Error   Drop MongoDB Collection    capif    user
	Run Keyword And Ignore Error   Drop MongoDB Collection    capif    serviceapidescriptions

	Disconnect From MongoDB