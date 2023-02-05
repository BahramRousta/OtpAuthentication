# Pull base image
FROM python:3.8-slim-buster

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD 1

COPY ./web /web

WORKDIR /web

COPY ./requirements.txt /web/requirements.txt

RUN pip install -r /web/requirements.txt