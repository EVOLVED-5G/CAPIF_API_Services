*** Settings ***
Library     /opt/robot-tests/tests/libraries/helpers.py

*** Variables ***

*** Keywords ***
Initialize Test And Register
	[Arguments]    ${password}=password    ${username}=robot    ${role}=invoker    ${description}=Testing    ${db_col}=

    Reset Db                     ${db_col}
    Register User At Jwt Auth    password=${password}    username=${username}    role=${role}    description=${description}

Reset Db
	[Arguments]    ${db_col}
	Log            Db capif.invokerdetails collection will be removed in order to isolate each test.

	Clean Test Information By HTTP Requests
	