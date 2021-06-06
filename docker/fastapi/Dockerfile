# https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi
# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY ./app /app

RUN cd /app && pip install -r requirements.txt