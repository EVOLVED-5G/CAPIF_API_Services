FROM nginx:latest
RUN apt-get update && apt-get install -y jq && apt-get clean
RUN apt-get install -y openssl

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./nginx_prepare.sh .

CMD ["sh", "nginx_prepare.sh"]
