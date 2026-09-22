FROM python:3.12-slim

WORKDIR /app

RUN pip install pika

COPY app.py .

ENTRYPOINT ["python", "app.py"]
