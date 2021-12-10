import pika
import json
import uuid

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(
    exchange='order',
    exchange_type='direct'
)

order = {
    'id': str(uuid.uuid4()),
    'user_email': 'vinicius@saturnino.com',
    'debit': 'IPVA 2022 | Licensing',
    'ipva_amount': 325.57,
    'licensing_amount': 198.32
}

bill = {
    'bill_id': str(uuid.uuid4()),
    'name': 'Vinicius de Sousa Saturnino',
    'cpf': '14458566423',
    'order': order,
    'total_amount': order.get('ipva_amount') + order.get('licensing_amount')
}

channel.basic_publish(
    exchange='order',
    routing_key='order.notify',
    body=json.dumps({ 'user_email': order['user_email'] })
)
print(' [x] Sent notify message')

channel.basic_publish(
    exchange='order',
    routing_key='order.report',
    body=json.dumps(order)
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
        body=json.dumps(bill)
    )
    print("THANK YOU FOR PAY YOUR DEBITS")
elif payment == 2:
    print("====== BYE !! :)) ======")

connection.close()
