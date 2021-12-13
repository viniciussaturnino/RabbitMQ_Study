import uuid


ORDER = {
    'id': str(uuid.uuid4()),
    'user_email': 'vinicius@saturnino.com',
    'debit': 'IPVA 2022 | Licensing',
    'ipva_amount': 325.57,
    'licensing_amount': 198.32
}

BILL = {
    'bill_id': str(uuid.uuid4()),
    'name': 'Vinicius de Sousa Saturnino',
    'cpf': '14458566423',
    'order': ORDER,
    'total_amount': ORDER.get('ipva_amount') + ORDER.get('licensing_amount')
}