#!/bin/bash
docker-compose -f "docker-compose-capif.yml" down  --rmi all --remove-orphans
docker network rm capif-network

status=$?
if [ $status -eq 0 ]; then
    echo "*** All Capif services are cleaned ***"
else
    echo "*** Some Capif services failed on clean ***"
fi

exit $status
