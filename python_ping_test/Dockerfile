
FROM ubuntu:latest

LABEL description="Ping Test"
LABEL version="0.1"
LABEL maintainer="sp-solutions@paloaltonetworks.com"

COPY requirements.txt /app/requirements.txt

RUN apt-get -y update \
    && apt-get -y install python3-pip \
    && pip3 install --upgrade pip \
    && pip3 install --no-cache-dir -r app/requirements.txt \
    && rm -rf /var/lib/apt/lists/*

