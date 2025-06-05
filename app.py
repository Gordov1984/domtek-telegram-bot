from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import openai
import os

app = Flask(__name__)

# Получаем токены из переменных среды
TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = "https://domtek-assistant.onrender.com"  # ЗАМЕНИ если адрес другой

openai.api_key = OPENAI_KEY

# Обработка входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

# Инициализация Telegram-приложения
@app.before_first_request
def start_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем вебхук
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=WEBHOOK_URL
    )

# Маршрут для Render проверки
@app.route('/')
def index():
    return 'Бот работает!'

# Запуск Flask
if __name__ == '__main__':
    app.run()
