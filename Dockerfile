# Usa uma imagem oficial do Python leve como base
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala a biblioteca pika para comunicação com o RabbitMQ
RUN pip install pika

# Copia o código da aplicação para dentro do container
COPY app.py .

# Define o comando base executado ao iniciar o container
ENTRYPOINT ["python", "app.py"]
