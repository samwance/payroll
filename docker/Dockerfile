FROM python:3.11.8-alpine3.19

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk add --no-cache postgresql-dev libpq

RUN addgroup -S app && adduser -S app -G app

COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir poetry==1.4.2 && \
    poetry install --no-dev

COPY . .

USER app
