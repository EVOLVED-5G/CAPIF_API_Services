*** Settings ***
Library     /opt/robot-tests/tests/libraries/helpers.py
Resource    /opt/robot-tests/common/customKeywords/utils.robot
Library     MongoDBLibrary

*** Variables ***


*** Keywords ***
Initialize Test And Register
	[Arguments]    ${password}=password    ${username}=robot    ${role}=invoker    ${description}=Testing    ${db_col}=

    Reset Db                     ${db_col}
    Register User At Jwt Auth    password=${password}    username=${username}    role=${role}    description=${description}

Reset Db
	[Arguments]           ${db_col}
	Log                   Db capif.invokerdetails collection will be removed in order to isolate each test.
	Connect To MongoDB    mongodb://root:example@localhost	27017

	@{allCollections}=            Get MongoDB Collections    capif
	Log Many	@{allCollections}

	Drop MongoDB Collection    capif    ${db_col}
	Drop MongoDB Collection    capif    user

	Disconnect From MongoDB