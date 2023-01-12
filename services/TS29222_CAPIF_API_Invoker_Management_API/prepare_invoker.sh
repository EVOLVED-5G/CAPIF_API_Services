#!/bin/bash

sleep 20
redis-cli -h redis -p 6379 -n 1 GET  server_pub_key > /usr/src/app/api_invoker_management/pubkey.pem

cd /usr/src/app/
python3 -m api_invoker_management