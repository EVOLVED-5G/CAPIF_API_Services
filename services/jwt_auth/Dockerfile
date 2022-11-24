FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt

RUN apk add -U --no-cache gcc build-base linux-headers ca-certificates libffi-dev libressl-dev libxslt-dev
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apk add redis

COPY . /usr/src/app

EXPOSE 8080

CMD ["sh", "register_prepare.sh"]
