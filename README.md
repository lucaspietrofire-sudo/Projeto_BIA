# Projeto BIA - Arquitetura Baseada em Eventos com RabbitMQ e Docker

Este projeto consiste numa demonstração prática e containerizada de uma Arquitetura Orientada a Eventos (EDA) assíncrona. O sistema utiliza Python, RabbitMQ como message broker e Docker Compose para a orquestração da infraestrutura, contando ainda com uma pipeline de CI/CD automatizada através do GitHub Actions.

---

## 1. Arquitetura e Componentes

O projeto é estruturado em três serviços isolados que comunicam entre si através de uma rede virtual criada pelo Docker:

* Broker (rabbitmq_bia):
  Serviço principal do RabbitMQ utilizando a imagem oficial rabbitmq:3-management. Expõe a porta 5672 para comunicação via protocolo AMQP e a porta 15672 para o painel de gestão visual no navegador.

* Produtor (produtor_bia):
  Serviço em Python responsável por publicar eventos formatados em JSON na fila fila_bia. Utiliza propriedades de persistência para garantir que as mensagens não sejam perdidas caso o broker seja reiniciado.

* Consumidor (consumidor_bia):
  Serviço em Python que permanece em execução contínua a escutar a fila fila_bia. Processa as mensagens recebidas e envia a confirmação de recebimento (acknowledgment / ack) de volta ao broker.

---

## 2. Pré-requisitos

Para executar este projeto num ambiente local, é necessário ter instalado:

* Docker
* Docker Compose
* Git

---

## 3. Como Executar com Docker Compose

1. Clonar o repositório:
   git clone https://github.com/lucaspietrofire-sudo/Projeto_BIA.git
   cd Projeto_BIA

2. Construir as imagens e iniciar os containers:
   docker compose up --build

3. Aceder ao Painel de Gestão do RabbitMQ:
   URL: http://localhost:15672
   Utilizador padrão: guest
   Palavra-passe padrão: guest

---

## 4. Teste Manual em Ambiente Local

Para testar o funcionamento dos scripts Python diretamente fora dos containers:

1. Instalar a biblioteca cliente AMQP:
   pip install pika

2. Iniciar o consumidor num terminal (permanecerá no aguardo de eventos):
   python app.py receber

3. Executar o produtor noutro terminal para publicar um evento:
   python app.py enviar

---

## 5. Integração Contínua (CI)

O repositório possui uma pipeline configurada através do GitHub Actions (.github/workflows/ci.yml). Este workflow valida automaticamente a sintaxe do ficheiro docker-compose.yml a cada envio (push) ou pedido de integração (pull request) realizado no ramo main.
