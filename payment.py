import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare('order_payment')
queue_name = queue.method.queue

channel.queue_bind(
    exchange='order',
    queue=queue_name,
    routing_key='order.payment'
)


def callback(ch, method, properties, body):
    payload = json.loads(body)
    print(' [x] Generating payment')
    print('\n====== Pending Bill ======\n')
    print(f"""
        BILL_ID: {payload.get('bill_id')}
        NAME: {payload.get('name')}
        CPF: {payload.get('cpf')}
        EMAIL: {payload.get('order').get('user_email')}
        ORDER:
            \tDEBITS: {payload.get('order').get('debit')}
            \tIPVA 2022: {payload.get('order').get('ipva_amount')}
            \tLICENSING: {payload.get('order').get('licensing_amount')}
        TOTAL_AMOUNT: {payload.get('total_amount')}
    """)
    print(' [x] Done\n')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_message_callback=callback, queue=queue_name)

print(' [*] Waiting for payment messages. To exit press Ctrl+C')

channel.start_consuming()
