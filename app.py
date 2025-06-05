from flask import Flask, request
import openai
import telegram
from telegram.ext import Application, MessageHandler, filters
import os

# Получаем токены из переменных окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Flask-приложение для Render
app = Flask(__name__)

@app.route('/')
def index():
    return 'Бот работает!'

# Telegram логика
async def handle_message(update, context):
    try:
        user_message = update.message.text
        print(f"Пользователь написал: {user_message}")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}],
            api_key=OPENAI_KEY
        )
        reply = response.choices[0].message["content"]
        await update.message.reply_text(reply)

    except Exception as e:
        print(f"Ошибка при обработке сообщения: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуй ещё раз позже.")

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    run_bot()
