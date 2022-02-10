#!/bin/bash
docker-compose up --detach --remove-orphans --build
status=$?
if [ $status -eq 0 ]; then
    echo "*** All Capif services are running ***"
else
    echo "*** Some Capif services failed to start ***"
fi

exit $status
