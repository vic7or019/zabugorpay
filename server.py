from flask import Flask, redirect, request
import requests

app = Flask(__name__)

@app.route('/payment')
def payment():
    amount = request.args.get('amount', default='100.00', type=str)
    
    payment_data = {
        'project_id': '01918faf-a5ab-7af7-a3fe-b0478bda0038',  # Ваш реальный project_id
        'amount': amount,
        'currency': 'RUB',
        'metadata': {
            'id': 123  # Уникальный идентификатор пользователя
        },
        'redirect_url': 'https://zabugorpay.ru/success'  # Ссылка для перенаправления после успешной оплаты
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Key': 'MgvW8WkUwOBTyXVAt6fg8qN7zfNEn579gcWsFnzpJ0rntrTw'  # Ваш реальный API-ключ
    }

    response = requests.post('https://rub.change.pro/api/payments', json=payment_data, headers=headers)

    if response.status_code == 201:
        payment_url = response.json()['data']['payment_url']
        return redirect(payment_url)
    else:
        return 'Ошибка при создании платежа', 400

if __name__ == '__main__':
    app.run(port=5000)
