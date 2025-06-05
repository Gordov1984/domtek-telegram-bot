import os
from flask import Flask, request
import telegram
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import openai
import asyncio

TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

@app.route('/')
def index():
    return 'Бот работает!'

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    asyncio.run(handle_message(update, None))
    return 'ok'

async def handle_message(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}],
        api_key=OPENAI_KEY
    )
    reply = response.choices[0].message["content"]
    await update.message.reply_text(reply)

async def set_webhook():
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    await bot.set_webhook(url=webhook_url)

if __name__ == '__main__':
    asyncio.run(set_webhook())
    app.run(host='0.0.0.0', port=10000)
