from flask import Flask, redirect, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Добавляем CORS для разрешения внешних запросов

# Установите токен вашего бота
TELEGRAM_TOKEN = '7300877680:AAFMDFouNAdvJXD3n8akwUBqyPUQ_Xz2iaQ'

def send_telegram_notification(order_id, amount, status):
    """Отправка уведомления в Telegram о статусе платежа всем пользователям."""
    message = f"Платеж по заказу {order_id} на сумму {amount} рублей. Статус: {status}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    # Читаем все chat_id из файла и отправляем сообщение каждому
    try:
        with open("chat_ids.txt", "r") as file:
            chat_ids = file.readlines()
        
        for chat_id in chat_ids:
            chat_id = chat_id.strip()  # Удаляем пробелы и символы новой строки
            payload = {
                'chat_id': chat_id,
                'text': message
            }
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                print(f"Ошибка при отправке уведомления в Telegram: {response.text}")
    except FileNotFoundError:
        print("Файл chat_ids.txt не найден. Убедитесь, что он существует.")

@app.route('/')
def home():
    try:
        return 'Сервер работает!'
    except Exception as e:
        print(f"Ошибка: {e}")
        return 'Ошибка на сервере', 500

@app.route('/payment')
def payment():
    amount = request.args.get('amount', default='100.00', type=str)
    order_id = request.args.get('order_id', default='0000', type=str)

    # Создаем метаданные с order_id
    metadata = {
        "order_id": order_id
    }

    payment_data = {
        'project_id': '0193781c-f938-7a6c-bf49-fbc3e4f7c144',  # Ваш реальный project_id
        'amount': amount,
        'currency': 'RUB',
        'metadata': metadata,
        'webhook_url': 'http://90.156.150.15:5000/payment-status'  # URL для вебхуков
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
        error_message = response.json().get('error', 'Неизвестная ошибка')
        print(f"Ошибка создания платежа: {error_message}")
        return f"Ошибка при создании платежа: {error_message}", 400

# Новый эндпоинт для обработки вебхуков от платежной системы
@app.route('/payment-status', methods=['POST'])
def payment_status():
    data = request.json

    # Извлекаем информацию из запроса
    event_name = data.get('event_name')
    payment_data = data.get('data', {})
    order_id = payment_data.get('metadata', {}).get('order_id')
    status = payment_data.get('status')
    amount = payment_data.get('amount')

    # Логика обработки статуса оплаты
    if event_name == "payment.completed":
        # Отправляем уведомление в Telegram о завершенной оплате
        send_telegram_notification(order_id, amount, status)
    else:
        print(f"Получено событие {event_name} для заказа {order_id} с суммой {amount} рублей. Статус: {status}")

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Сервер доступен на всех интерфейсах с портом 5000
