FROM python:alpine3.6
MAINTAINER Gabriel Ecker <gabriel.ecker@gmail.com>

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY . /code

RUN apk update \
    && apk add --update gcc postgresql make jpeg \
    && apk add --update --virtual build-deps \
    python3-dev \
    musl-dev \
    postgresql-dev \
    jpeg-dev \
    zlib-dev \
    && pip install pipenv && pipenv install --dev  \
    && apk del build-deps \
    && mv docker-entrypoint.sh /usr/local/bin/ \
    && chmod +x /usr/local/bin/docker-entrypoint.sh \
    && ln -s /usr/local/bin/docker-entrypoint.sh /
