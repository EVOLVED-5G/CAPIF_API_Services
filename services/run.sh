#!/bin/bash
HOSTNAME=capifcore
DEPLOY=all


echo Nginx hostname will be $HOSTNAME and deploy $DEPLOY

docker network create capif-network

docker-compose -f "docker-compose-easy-rsa.yml"  up --detach --build

status=$?
if [ $status -eq 0 ]; then
    echo "*** Easy RSA Service Runing ***"
else
    echo "*** Easy RSA failed to start ***"
    exit $status
fi



CAPIF_HOSTNAME=$HOSTNAME docker-compose -f "docker-compose-capif.yml"  up --detach --build

status=$?
if [ $status -eq 0 ]; then
    echo "*** All Capif services are running ***"
else
    echo "*** Some Capif services failed to start ***"
    exit $status
fi


CAPIF_PRIV_KEY_BASE_64=$(echo "$(cat nginx/certs/server.key)")
CAPIF_PRIV_KEY=$CAPIF_PRIV_KEY_BASE_64 docker-compose -f "docker-compose-register.yml"  up --detach --build

status=$?
if [ $status -eq 0 ]; then
    echo "*** Register Service are running ***"
else
    echo "*** Register Service failed to start ***"
fi

exit $status







