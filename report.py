import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare('order_report')
queue_name = queue.method.queue

channel.queue_bind(
    exchange='order',
    queue=queue_name,
    routing_key='order.report'
)


def callback(ch, method, properties, body):
    payload = json.loads(body)
    print(' [x] Generating report')
    print(f"""
        ID: {payload.get('id')}
        User Email: {payload.get('user_email')}
        Debit: {payload.get('debit')}
        IPVA 2022: {payload.get('ipva_amount')}
        Licensing: {payload.get('licensing_amount')}
    """)
    print(' [x] Done\n')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_message_callback=callback, queue=queue_name)

print(' [*] Waiting for report messages. To exit press Ctrl+C')

channel.start_consuming()
