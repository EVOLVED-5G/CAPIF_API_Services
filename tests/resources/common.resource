*** Settings ***
Library     /opt/robot-tests/tests/libraries/helpers.py
Resource    /opt/robot-tests/common/customKeywords/utils.robot
Library    MongoDBLibrary

*** Variables ***


*** Keywords ***
Initialize Test And Register
	[Arguments]    ${email}=robot@test.com    ${password}=password    ${username}=robot    ${hostip}=localhost    ${role}=invoker
    Reset Db
    Register User At Jwt Auth

Reset Db
	Log                   Db capif.invokerdetails collection will be removed in order to isolate each test.
	Connect To MongoDB    mongodb://root:example@localhost	27017

	@{allCollections}=             Get MongoDB Collections    capif
	Log Many	@{allCollections}

	Drop MongoDB Collection    capif    invokerdetails
	Drop MongoDB Collection    capif    user

	Disconnect From MongoDB