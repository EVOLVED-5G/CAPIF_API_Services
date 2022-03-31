FROM nginx
RUN apt-get update && apt-get install -y jq && apt-get clean

COPY ./nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
