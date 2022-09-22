FROM python:3.8-slim-buster
LABEL maintainer="Jorge Moratinos Salcines <jorge.moratinossalcines@telefonica.com>"
LABEL version="1.0"
LABEL description="Docker to run EasyRSA"

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /root

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y --no-install-recommends  wget openssl


RUN wget --no-check-certificate -P ~/ https://github.com/OpenVPN/easy-rsa/releases/download/v3.0.4/EasyRSA-3.0.4.tgz

RUN tar xvf EasyRSA-3.0.4.tgz
RUN rm EasyRSA-3.0.4.tgz
COPY vars EasyRSA-3.0.4/vars

RUN echo 'PATH="EasyRSA-3.0.4/:$PATH"' >> .profile

RUN EasyRSA-3.0.4/easyrsa init-pki
RUN yes | EasyRSA-3.0.4/easyrsa build-ca nopass

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod a+x *.sh

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "app"]
