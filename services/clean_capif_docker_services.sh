#!/bin/bash
docker-compose down --rmi all --remove-orphans
status=$?
if [ $status -eq 0 ]; then
    echo "*** All Capif services are cleaned ***"
else
    echo "*** Some Capif services failed on clean ***"
fi

exit $status
