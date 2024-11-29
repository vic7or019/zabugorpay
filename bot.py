from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import uuid
import os
from datetime import datetime

TOKEN = '7300877680:AAFMDFouNAdvJXD3n8akwUBqyPUQ_Xz2iaQ'
PAYMENT_SERVER_URL = 'http://84.201.180.71:5000/payment'
CHAT_IDS_FILE = "chat_ids.txt"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if not os.path.exists(CHAT_IDS_FILE):
        with open(CHAT_IDS_FILE, "w") as file:
            pass

    try:
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
        order_id = str(uuid.uuid4())
        payment_url = f"{PAYMENT_SERVER_URL}?amount={amount}&order_id={order_id}"

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order_message = f"Создан заказ номер {order_id} на сумму {amount} рублей в {now}."

        await update.message.reply_text(order_message)

        keyboard = [[InlineKeyboardButton("Перейти к оплате", url=payment_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(f'Для оплаты {amount} рублей нажмите кнопку ниже:', reply_markup=reply_markup)
    except ValueError:
        await update.message.reply_text('Пожалуйста, введите корректную сумму.')
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {str(e)}')


def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount))
    application.run_polling()


if __name__ == '__main__':
    main()
