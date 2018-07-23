FROM python:3.7-slim

WORKDIR /app

RUN pip install --trusted-host pypi.python.org \
  Flask iso8601 pytest pyyaml requests

EXPOSE 80
