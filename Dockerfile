FROM python:alpine3.6
MAINTAINER Gabriel Ecker <gabriel.ecker@gmail.com>

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY Pipfile Pipfile.lock /code/
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql postgresql-dev jpeg-dev zlib-dev make \
    && pip install pipenv && pipenv install --dev

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh \
    && ln -s /usr/local/bin/docker-entrypoint.sh /

ADD . /code/