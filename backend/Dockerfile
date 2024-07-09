FROM python:3.10-alpine

WORKDIR /app

# Instala dependencias necesarias para construir MySQLdb

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
