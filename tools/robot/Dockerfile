FROM harbor.elevenpaths.com/dockerhub-proxy/library/alpine:3.12.1
LABEL maintainer="Jorge Moratinos Salcines <jorge.moratinossalcines@telefonica.com>"
LABEL version="1.0"
LABEL description="Docker to run Robot Framework"

ENV ROBOT_DIRECTORY=/opt/robot-tests
ENV ROBOT_COMMON_DIRECTORY=$ROBOT_DIRECTORY/common
ENV ROBOT_TESTS_DIRECTORY=$ROBOT_DIRECTORY/tests
ENV ROBOT_RESULTS_DIRECTORY=$ROBOT_DIRECTORY/results


# Create directories structure
RUN mkdir $ROBOT_DIRECTORY
RUN mkdir $ROBOT_COMMON_DIRECTORY
RUN mkdir $ROBOT_TESTS_DIRECTORY
RUN mkdir $ROBOT_RESULTS_DIRECTORY

# Create Volumes for docker
# VOLUME $ROBOT_DIRECTORY
VOLUME $ROBOT_COMMON_DIRECTORY
VOLUME $ROBOT_TESTS_DIRECTORY
VOLUME $ROBOT_RESULTS_DIRECTORY

WORKDIR $ROBOT_DIRECTORY

# Install dependencies
RUN apk upgrade
RUN apk --update --no-cache add \
    build-base \
    bash \
    bash-completion \
    libxml2 \
    libxslt \
    curl \
    yarn \
    less \
    dpkg \
    wget \
    python3 \
    python3-dev \
    libxslt-dev \
    libffi-dev \
    py-pip \
    openssl-dev \
    openldap-dev \
    python2-dev

RUN mkdir /opt/venv
RUN python3 -m venv /opt/venv

ADD basicRequirements.txt /root/

ADD basicRobotInstall.sh /root/
RUN chmod a+x /root/basicRobotInstall.sh \
    && /root/basicRobotInstall.sh /root/basicRequirements.txt
RUN sed -i 's/\/bin\/ash/\/bin\/bash/g' /etc/passwd

ADD entrypoint.sh /root/
ADD linter_entrypoint.sh /root/
ADD featdoc_entrypoint.sh /root/
ADD libdoc_entrypoint.sh /root/


RUN sed  -i 's|ROBOT_DIRECTORY|'$ROBOT_DIRECTORY'|g' /root/entrypoint.sh
RUN sed  -i 's|ROBOT_TESTS_DIRECTORY|'$ROBOT_TESTS_DIRECTORY'|g' /root/entrypoint.sh
RUN sed  -i 's|ROBOT_COMMON_DIRECTORY|'$ROBOT_COMMON_DIRECTORY'|g' /root/entrypoint.sh
RUN sed  -i 's|ROBOT_RESULTS_DIRECTORY|'$ROBOT_RESULTS_DIRECTORY'|g' /root/entrypoint.sh

RUN sed  -i 's|ROBOT_DIRECTORY|'$ROBOT_DIRECTORY'|g' /root/linter_entrypoint.sh
RUN sed  -i 's|ROBOT_TESTS_DIRECTORY|'$ROBOT_TESTS_DIRECTORY'|g' /root/linter_entrypoint.sh
RUN sed  -i 's|ROBOT_COMMON_DIRECTORY|'$ROBOT_COMMON_DIRECTORY'|g' /root/linter_entrypoint.sh


RUN sed  -i 's|ROBOT_DIRECTORY|'$ROBOT_DIRECTORY'|g' /root/featdoc_entrypoint.sh
RUN sed  -i 's|ROBOT_TESTS_DIRECTORY|'$ROBOT_TESTS_DIRECTORY'|g' /root/featdoc_entrypoint.sh
RUN sed  -i 's|ROBOT_COMMON_DIRECTORY|'$ROBOT_COMMON_DIRECTORY'|g' /root/featdoc_entrypoint.sh

RUN sed  -i 's|ROBOT_DIRECTORY|'$ROBOT_DIRECTORY'|g' /root/libdoc_entrypoint.sh
RUN sed  -i 's|ROBOT_TESTS_DIRECTORY|'$ROBOT_TESTS_DIRECTORY'|g' /root/libdoc_entrypoint.sh
RUN sed  -i 's|ROBOT_COMMON_DIRECTORY|'$ROBOT_COMMON_DIRECTORY'|g' /root/libdoc_entrypoint.sh




RUN chmod a+x /root/entrypoint.sh
RUN chmod a+x /root/linter_entrypoint.sh
RUN chmod a+x /root/featdoc_entrypoint.sh
RUN chmod a+x /root/libdoc_entrypoint.sh


ENTRYPOINT [ "/root/entrypoint.sh" ]
