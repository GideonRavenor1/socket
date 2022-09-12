FROM python:3.7.6-slim-stretch as build

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    gcc

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


FROM python:3.7.6-slim-stretch

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY --from=build /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/
COPY --from=build /usr/local/bin/ /usr/local/bin/
COPY . .