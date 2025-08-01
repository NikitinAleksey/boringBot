FROM python:3.11-slim

WORKDIR /boringBot

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /boringBot/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

ENV PYTHONPATH=/boringBot/app
ENV PYTHONDONTWRITEBYTECODE=1
