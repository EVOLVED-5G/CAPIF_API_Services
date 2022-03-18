FROM harbor.elevenpaths.com/dockerhub-proxy/library/ubuntu:18.04
LABEL maintainer="Jorge Moratinos Salcines <jorge.moratinossalcines@telefonica.com>"
LABEL version="1.0"
LABEL description="Docker to run EasyRSA"

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /root

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y --no-install-recommends  \
    wget \
    bash \
    bash-completion \
    openssh-server \
    openssl \
    sudo \
    curl \
    python3-pip \
    iproute2

RUN useradd -m -s /bin/bash adminca
RUN echo "adminca ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/adminca && \
    chmod 0440 /etc/sudoers.d/adminca

RUN su - adminca -c "wget --no-check-certificate -P ~/ https://github.com/OpenVPN/easy-rsa/releases/download/v3.0.4/EasyRSA-3.0.4.tgz"
RUN chown adminca:adminca /home/adminca/EasyRSA-3.0.4.tgz
RUN chmod 666 /home/adminca/EasyRSA-3.0.4.tgz
RUN su - adminca -c "tar xvf EasyRSA-3.0.4.tgz"
RUN su - adminca -c "rm EasyRSA-3.0.4.tgz"
COPY vars /home/adminca/EasyRSA-3.0.4/vars

RUN chown adminca:adminca /home/adminca/EasyRSA-3.0.4/vars
RUN chmod 664 /home/adminca/EasyRSA-3.0.4/vars
RUN su - adminca -c "echo 'PATH="/home/adminca/EasyRSA-3.0.4/:$PATH"' >> .profile"

RUN su - adminca -c "easyrsa init-pki"
RUN su - adminca -c "yes | easyrsa build-ca nopass"
RUN echo 'adminca:adminca' | chpasswd

RUN pip3 install requests

RUN service ssh start

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]

# docker exec -it $(docker ps -aqf "name=easy") bash
# cd /usr/src/app/
# python3 send_cert.py
