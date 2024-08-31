from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import requests
import random
import datetime

# Установите токен доступа
TOKEN = '7300877680:AAFMDFouNAdvJXD3n8akwUBqyPUQ_Xz2iaQ'
PAYMENT_SERVER_URL = 'http://51.250.47.64:5000/payment'

# Глобальная переменная для хранения суммы и order_id
user_payment_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите сумму, которую хотите оплатить:')

async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text)
        chat_id = update.message.chat_id

        # Генерируем уникальный order_id
        order_id = random.randint(1000, 9999)

        # Сохраняем данные
        user_payment_data[chat_id] = {'amount': amount, 'order_id': order_id}

        # Формируем ссылку на оплату
        payment_url = f"{PAYMENT_SERVER_URL}?amount={amount}&order_id={order_id}"
        keyboard = [[InlineKeyboardButton("Перейти к оплате", url=payment_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение с кнопкой оплаты
        await update.message.reply_text(f'Для оплаты {amount} рублей нажмите кнопку ниже:', reply_markup=reply_markup)

        # Отправляем сообщение с информацией о созданном заказе
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await update.message.reply_text(f'Создан заказ #{order_id} на сумму {amount} рублей в {now}.')
    except ValueError:
        await update.message.reply_text('Пожалуйста, введите корректную сумму.')

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Обработчик команды /start
    application.add_handler(CommandHandler('start', start))

    # Обработчик сообщений для ввода суммы
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount))

    application.run_polling()

if __name__ == '__main__':
    main()
