#!/bin/bash

OUTPUT=$(redis-cli -h redis -p 6379 -n 1 GET  server_priv_key)
echo "$OUTPUT"

if [ -z "$OUTPUT" ]; then
    echo "OUTPUT empty"
    exit 1;
else
    echo "OUTPUT: $OUTPUT"
    redis-cli -h redis -p 6379 -n 1 GET  server_priv_key > /usr/src/app/capif_security/server.key
fi

cd /usr/src/app/
python3 -m capif_security