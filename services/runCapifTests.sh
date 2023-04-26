#!/bin/bash

DOCKER_ROBOT_IMAGE=dockerhub.hi.inet/5ghacking/5gnow-robot-test-image
DOCKER_ROBOT_IMAGE_VERSION=4.0
cd ..
REPOSITORY_BASE_FOLDER=${PWD}
TEST_FOLDER=$REPOSITORY_BASE_FOLDER/tests
RESULT_FOLDER=$REPOSITORY_BASE_FOLDER/results
ROBOT_DOCKER_FILE_FOLDER=$REPOSITORY_BASE_FOLDER/tools/robot

# nginx Hostname and http port (80 by default) to reach for tests
CAPIF_HOSTNAME=capifcore
CAPIF_HTTP_PORT=8080
CAPIF_HTTPS_PORT=443

echo "HOSTNAME = $CAPIF_HOSTNAME"
echo "CAPIF_HTTP_PORT = $CAPIF_HTTP_PORT"
echo "CAPIF_HTTPS_PORT = $CAPIF_HTTPS_PORT"

docker >/dev/null 2>/dev/null
if [[ $? -ne 0 ]]
then
    echo "Docker maybe is not installed. Please check if docker CLI is present."
    exit -1
fi

docker images|grep -Eq '^'$DOCKER_ROBOT_IMAGE'[ ]+[ ]'$DOCKER_ROBOT_IMAGE_VERSION''
if [[ $? -ne 0 ]]
then
    read -p "Robot image is not present. To continue, Do you want to build it? (y/n)" build_robot_image
    if [[ $build_robot_image == "y" ]]
    then
        echo "Building Robot docker image."
        cd $ROBOT_DOCKER_FILE_FOLDER
        docker build  -t $DOCKER_ROBOT_IMAGE:$DOCKER_ROBOT_IMAGE_VERSION .
        cd $REPOSITORY_BASE_FOLDER
    else
        exit -2
    fi
fi

mkdir -p $RESULT_FOLDER

docker run -ti --rm --network="host" \
    -v $TEST_FOLDER:/opt/robot-tests/tests \
    -v $RESULT_FOLDER:/opt/robot-tests/results ${DOCKER_ROBOT_IMAGE}:${DOCKER_ROBOT_IMAGE_VERSION}  \
    --variable CAPIF_HOSTNAME:$CAPIF_HOSTNAME \
    --variable CAPIF_HTTP_PORT:$CAPIF_HTTP_PORT \
    --variable CAPIF_HTTPS_PORT:$CAPIF_HTTPS_PORT $@
