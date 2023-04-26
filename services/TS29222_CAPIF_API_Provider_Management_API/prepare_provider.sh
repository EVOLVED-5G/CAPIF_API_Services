#!/bin/bash

OUTPUT=$(redis-cli -h redis -p 6379 -n 1 GET  server_pub_key)
echo "$OUTPUT"

if [ -z "$OUTPUT" ]; then
    echo "OUTPUT empty"
    exit 1;
else
    echo "OUTPUT: $OUTPUT"
    redis-cli -h redis -p 6379 -n 1 GET  server_pub_key > /usr/src/app/api_provider_management/pubkey.pem
fi

cd /usr/src/app/
python3 -m api_provider_management