#!/bin/bash

sleep 10 
redis-cli -h redis -p 6379 -n 1 GET  server_priv_key > /usr/src/app/capif_security/server.key

cd /usr/src/app/
python3 -m capif_security