
FROM python:3.7-alpine

LABEL description="Ping Test"
LABEL version="0.1"
LABEL maintainer="sp-solutions@paloaltonetworks.com"

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r app/requirements.txt