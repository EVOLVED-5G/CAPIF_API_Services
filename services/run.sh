#!/bin/bash
HOSTNAME=capifcore
MONITORING_STATE=false
DEPLOY=all
DEPLOY_BACKOFFICE=${DEPLOY_BACKOFFICE:-true}

if [ "$1" = "--monitoring" ]; then
    if [ "$2" = "true" ]; then
        MONITORING_STATE=true
    elif [ "$2" = "false" ]; then
        MONITORING_STATE=false
    else
        echo "El valor para --monitoring debe ser 'true' o 'false'."
        exit 1
    fi
fi


echo Nginx hostname will be $HOSTNAME and deploy $DEPLOY

if [ "$MONITORING_STATE" = true ] ; then
    echo '***Monitoring set as true***'
    echo '***Creating Monitoging stack***'

    docker-compose -f "../monitoring/docker-compose.yml" up --detach
    status=$?
    if [ $status -eq 0 ]; then
        echo "*** Monitoring Stack Runing ***"
    else
        echo "*** Monitoring Stack failed to start ***"
        exit $status
    fi
fi

docker network create capif-network

docker-compose -f "docker-compose-easy-rsa.yml"  up --detach --build

status=$?
if [ $status -eq 0 ]; then
    echo "*** Easy RSA Service Runing ***"
else
    echo "*** Easy RSA failed to start ***"
    exit $status
fi



CAPIF_HOSTNAME=$HOSTNAME MONITORING=$MONITORING_STATE docker-compose -f "docker-compose-capif.yml"  up --detach --build

status=$?
if [ $status -eq 0 ]; then
    echo "*** All Capif services are running ***"
else
    echo "*** Some Capif services failed to start ***"
    exit $status
fi


CAPIF_PRIV_KEY_BASE_64="$(cat nginx/certs/server.key)"
CAPIF_PRIV_KEY=$CAPIF_PRIV_KEY_BASE_64 docker-compose -f "docker-compose-register.yml"  up --detach --build

status=$?
if [ $status -eq 0 ]; then
    echo "*** Register Service are running ***"
else
    echo "*** Register Service failed to start ***"
fi


if [ $DEPLOY_BACKOFFICE -eq false ]; then
    exit $status
fi


docker-compose -f "docker-compose-backoffice.yml"  up --detach --build

status=$?
if [ $status -eq 0 ]; then
    echo "*** Backoffice Service are running ***"
else
    echo "*** Backoffice Service failed to start ***"
fi

exit $status
