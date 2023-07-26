FROM python:3.11-alpine


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apk add poetry && poetry install --no-dev

WORKDIR /app

COPY . ./backend

RUN pip install --no-cache-dir -r requirements.txt
