FROM nginx:latest
RUN apt-get update && apt-get install -y jq && apt-get clean
RUN apt-get install -y openssl

RUN mkdir -p /etc/nginx/certs

COPY ./certs/sign_req_body_tmp.json /etc/nginx/certs/sign_req_body_tmp.json
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./nginx_prepare.sh .

CMD ["sh", "nginx_prepare.sh"]
