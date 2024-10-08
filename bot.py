from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import uuid
import os
from datetime import datetime

# Установите токен доступа
TOKEN = '7300877680:AAFMDFouNAdvJXD3n8akwUBqyPUQ_Xz2iaQ'
PAYMENT_SERVER_URL = 'http://51.250.47.64/payment'

# Путь к файлу chat_ids.txt
CHAT_IDS_FILE = "chat_ids.txt"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    # Проверяем, существует ли файл chat_ids.txt и создаем его, если нет
    if not os.path.exists(CHAT_IDS_FILE):
        with open(CHAT_IDS_FILE, "w") as file:
            pass  # создаем пустой файл

    try:
        # Проверяем, есть ли chat_id уже в файле
        with open(CHAT_IDS_FILE, "r") as file:
            chat_ids = file.readlines()

        if f"{chat_id}\n" not in chat_ids:
            with open(CHAT_IDS_FILE, "a") as file:
                file.write(f"{chat_id}\n")

        await update.message.reply_text('Введите сумму, которую хотите оплатить:')
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {str(e)}')

async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text)
        chat_id = update.message.chat_id
        user_payment_amount = {}  # Это локальная переменная, используется для хранения суммы
        user_payment_amount[chat_id] = amount

        order_id = str(uuid.uuid4())  # Генерируем уникальный order_id
        payment_url = f"{PAYMENT_SERVER_URL}?amount={amount}&order_id={order_id}"
        
        # Формируем сообщение с информацией о заказе
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order_message = f"Создан заказ номер {order_id} на сумму {amount} рублей в {now}."
        
        # Отправляем сообщение о создании заказа
        await update.message.reply_text(order_message)
        
        # Создаем и отправляем кнопку с ссылкой на оплату
        keyboard = [[InlineKeyboardButton("Перейти к оплате", url=payment_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(f'Для оплаты {amount} рублей нажмите кнопку ниже:', reply_markup=reply_markup)
    except ValueError:
        await update.message.reply_text('Пожалуйста, введите корректную сумму.')
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {str(e)}')

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Обработчик команды /start
    application.add_handler(CommandHandler('start', start))

    # Обработчик сообщений для ввода суммы
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount))

    application.run_polling()

if __name__ == '__main__':
    main()
