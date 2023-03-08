FROM python:3.8-slim-buster
LABEL maintainer="Jorge Moratinos Salcines <jorge.moratinossalcines@telefonica.com>"
LABEL version="1.0"
LABEL description="Docker to run EasyRSA"

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /root

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod a+x *.sh

EXPOSE 8080

WORKDIR /root/certs
CMD ["sh", "/root/certs/prepare_easy_rsa.sh"]
