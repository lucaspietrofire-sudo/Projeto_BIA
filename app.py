import pika
import sys
import json
import os

def conectar():
    host_rabbit = os.environ.get('RABBITMQ_HOST', 'localhost')
    
    conexao = pika.BlockingConnection(pika.ConnectionParameters(host=host_rabbit))
    return conexao, conexao.channel()

def enviar_evento():
    conexao, channel = conectar()

    # Garante que a fila continue existindo mesmo se o RabbitMQ reiniciar
    channel.queue_declare(queue='fila_bia', durable=True)
    
    evento = {"projeto": "BIA", "status": "Gerar relatorio"}
    
    channel.basic_publish(
        exchange='',
        routing_key='fila_bia',
        body=json.dumps(evento),
        properties=pika.BasicProperties(delivery_mode=2)    # delivery_mode=2 torna a mensagem persistente no disco
    )
    print("[PRODUTOR] Evento enviado para a fila!")
    conexao.close()

def iniciar_consumidor():
    conexao, channel = conectar()
    channel.queue_declare(queue='fila_bia', durable=True)
    
    print('Aguardando mensagens. Para simular que o sistema CAIU, aperte CTRL+C.')

    def callback(ch, method, properties, body):
        dados = json.loads(body)
        print(f"[CONSUMIDOR] Evento recebido: {dados['status']}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='fila_bia', on_message_callback=callback)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nO consumidor foi DESLIGADO (Simulação de falha).")
        conexao.close()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'enviar':
        enviar_evento()
    elif len(sys.argv) > 1 and sys.argv[1] == 'receber':
        iniciar_consumidor()
    else:
        print("Use: python3 app.py enviar  OU  python3 app.py receber")