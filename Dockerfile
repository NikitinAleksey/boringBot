FROM python:3.11

WORKDIR /boringBot

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    unzip \
    && curl -s https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip -o /tmp/ngrok.zip \
    && unzip /tmp/ngrok.zip -d /usr/local/bin \
    && rm /tmp/ngrok.zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /boringBot/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

ENV PYTHONPATH=/boringBot/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV NGROK_CONFIG=/tmp/ngrok.yml

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]