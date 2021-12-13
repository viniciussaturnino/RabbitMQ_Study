import pika
import json

from mock.order_mock import BILL, ORDER

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(
    exchange='order',
    exchange_type='direct'
)

channel.basic_publish(
    exchange='order',
    routing_key='order.notify',
    body=json.dumps({ 'user_email': ORDER['user_email'] })
)
print(' [x] Sent notify message')

channel.basic_publish(
    exchange='order',
    routing_key='order.report',
    body=json.dumps(ORDER)
)
print(' [x] Sent report message')

print('\n======== PAY DEBIT ========\n')
print('(1) YES')
print('(2) NOT YET')

payment = int(input())

if payment == 1:
    channel.basic_publish(
        exchange='order',
        routing_key='order.payment',
        body=json.dumps(BILL)
    )
    print("THANK YOU FOR PAY YOUR DEBITS")
elif payment == 2:
    print("====== BYE !! :)) ======")

connection.close()
