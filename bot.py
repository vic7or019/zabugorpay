from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# Установите токен доступа
TOKEN = '7300877680:AAFMDFouNAdvJXD3n8akwUBqyPUQ_Xz2iaQ'
PAYMENT_SERVER_URL = 'http://51.250.47.64/payment'

# Глобальная переменная для хранения chat_id всех пользователей
user_chat_ids = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_chat_ids.add(chat_id)  # Сохраняем chat_id пользователя
    await update.message.reply_text('Введите сумму, которую хотите оплатить:')

async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text)
        chat_id = update.message.chat_id
        user_payment_amount = {}  # Это локальная переменная, используется для хранения суммы
        user_payment_amount[chat_id] = amount

        order_id = "1234"  # Здесь можно динамически генерировать уникальный order_id
        payment_url = f"{PAYMENT_SERVER_URL}?amount={amount}&order_id={order_id}"
        keyboard = [[InlineKeyboardButton("Перейти к оплате", url=payment_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(f'Для оплаты {amount} рублей нажмите кнопку ниже:', reply_markup=reply_markup)
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
