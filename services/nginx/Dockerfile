FROM nginx:1.23.1
RUN apt-get update && apt-get install -y jq && apt-get clean
RUN apt-get install -y openssl
RUN apt-get install -y curl=7.74.0-1.3+deb11u3
RUN apt-get -y install redis


RUN mkdir -p /etc/nginx/certs

COPY ./certs/sign_req_body_tmp.json /etc/nginx/certs/sign_req_body_tmp.json
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./nginx_prepare.sh .

RUN chmod a+x nginx_prepare.sh

CMD ["sh", "nginx_prepare.sh"]
