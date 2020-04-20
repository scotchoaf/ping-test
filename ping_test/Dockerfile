
FROM python:slim-buster

LABEL description="Ping Test"
LABEL version="0.1"
LABEL maintainer="sp-solutions@paloaltonetworks.com"

COPY requirements.txt /app/requirements.txt

RUN apt-get -y update && pip install --upgrade pip \
    && pip install --no-cache-dir -r app/requirements.txt \
    && apt-get -y install iputils-ping \
    && rm -rf /var/lib/apt/lists/*