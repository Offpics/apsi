FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install -r requirements.txt