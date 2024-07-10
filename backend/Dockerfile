# Dockerfile for backend
FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache \
    gcc \
    musl-dev \
    mariadb-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Fix flask_mysqldb to be compatible with Flask 3.0.0
RUN sed -i 's/_app_ctx_stack/g/' /usr/local/lib/python3.10/site-packages/flask_mysqldb/__init__.py

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
