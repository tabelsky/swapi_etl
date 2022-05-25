FROM python:3.9.13-alpine3.15
COPY app /
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
WORKDIR app

ENTRYPOINT sh entrypoint.sh