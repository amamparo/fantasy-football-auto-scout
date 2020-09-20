FROM python:3.7.5-slim

MAINTAINER Aaron Mamparo

ARG PROXY_PORT
ENV PROXY_PORT="${PROXY_PORT}"

WORKDIR /app
ADD . /app
RUN apt-get update && apt-get install -y --no-install-recommends curl
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install
EXPOSE "${PROXY_PORT}"
CMD ["pipenv", "run", "python", "-u", "-m", "src.yahoo_proxy.server"]