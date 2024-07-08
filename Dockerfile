FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY ./backend /app

CMD ["gunicorn", "--config", "backend/gconfig.py", "'backend.app:app'" ]