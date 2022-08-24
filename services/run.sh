#!/bin/bash
HOSTNAME=capifcore
if [ "$#" -eq 1 ]; then
    HOSTNAME=$1
fi
echo Nginx hostname will be $HOSTNAME

CAPIF_HOSTNAME=$HOSTNAME docker-compose up --detach --remove-orphans --build
status=$?
if [ $status -eq 0 ]; then
    echo "*** All Capif services are running ***"
else
    echo "*** Some Capif services failed to start ***"
fi

exit $status
