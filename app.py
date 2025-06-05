from flask import Flask, request
import openai
import telegram
from telegram.ext import Application, MessageHandler, filters
import os

# Токены
TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Хендлер
async def handle_message(update, context):
    user_message = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}],
        api_key=OPENAI_KEY
    )
    reply = response.choices[0].message["content"]
    await update.message.reply_text(reply)

# Запуск
def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

@app.route('/')
def index():
    return 'Бот работает!'

if __name__ == '__main__':
    run_bot()
