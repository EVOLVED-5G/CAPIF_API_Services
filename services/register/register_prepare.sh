#!/bin/bash

# sleep 10
# redis-cli -h redis -p 6379 -n 1 GET  server_priv_key > /usr/src/app/register_service/server.key

destdir=/usr/src/app/register_service/server.key
echo "$CAPIF_PRIV_KEY" > "$destdir"
cd /usr/src/app/
python3 -m register_service