#!/bin/bash

ENDPOINTS=()
SERVICE_NAMES=()
COMPOSITE_PROJECT=CAPIF-composite-test2
OUTPUT_HOST_BASE_DIRECTORY=out/CAPIF-composite-test2
OUTPUT_DOCKER_BASE_DIRECTORY=/gen/$OUTPUT_HOST_BASE_DIRECTORY
DOCKER_COMPOSE_FILENAME=$OUTPUT_HOST_BASE_DIRECTORY/docker-compose-test.yml
NGINX_CONF_FILE=$OUTPUT_HOST_BASE_DIRECTORY/nginx.conf

echo "docker compose file: $DOCKER_COMPOSE_FILENAME"
mkdir -p $OUTPUT_HOST_BASE_DIRECTORY

# rm $DOCKER_COMPOSE_FILENAME || true
cat > $DOCKER_COMPOSE_FILENAME << EOF
services:
EOF

function createPythonServer {
    SWAGGER_FILE=$1
    API_NAME=$(basename -s .yaml $SWAGGER_FILE)
    ENDPOINT=$(awk '/- url: /{ print $3 }' $SWAGGER_FILE|awk -F / '{ print $2}')
    OUTPUT=$OUTPUT_DOCKER_BASE_DIRECTORY/$API_NAME/
    echo "SWAGGER_FILE: $SWAGGER_FILE"
    echo "API_NAME: $API_NAME"
    echo "ENDPOINT: $ENDPOINT"
    echo "OUTPUT DIRECTORY: $OUTPUT"
    ENDPOINTS+=($ENDPOINT)
    SERVICE_NAME=$(echo $ENDPOINT | sed 's/-/_/g')
    # SERVICE_NAMES+=($SERVICE_NAME)
    ./run-in-docker.sh generate -i $SWAGGER_FILE \
       -g python-flask \
       -o $OUTPUT \
       --package-name=$SERVICE_NAME
    cat >> $DOCKER_COMPOSE_FILENAME << EOF
  $ENDPOINT:
    build: $API_NAME/.
    expose:
      - "8080"
EOF
}


CAPIF_FILES=$(ls capif|awk '/TS29222/{  print "capif/"$0 }')
for CAPIF_FILE in ${CAPIF_FILES[*]}
do
createPythonServer $CAPIF_FILE
done

cat >> $DOCKER_COMPOSE_FILENAME << EOF
  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "8080:8080"
    depends_on:
EOF

for endpoint in ${ENDPOINTS[*]}
do
cat >> $DOCKER_COMPOSE_FILENAME << EOF
      - $endpoint
EOF
done

cat > $NGINX_CONF_FILE << EOF
user  nginx;

events {
    worker_connections   1000;
}
http {
        server {
              listen 8080;
EOF


for endpoint in ${ENDPOINTS[*]}
do
cat >> $NGINX_CONF_FILE << EOF
              location /$endpoint {
                proxy_pass http://$endpoint:8080;
              }
EOF
done

cat >> $NGINX_CONF_FILE << EOF
        }
}
EOF

