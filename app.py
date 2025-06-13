import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text or "Файл получен!" if update.message.document or update.message.photo else "?"
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ты написал: {text}")

dispatcher.add_handler(MessageHandler(Filters.all, handle_message))

@app.route('/')
def home():
    return 'Bot is alive!', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return 'ok', 200

if __name__ == '__main__':
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host='0.0.0.0', port=10000)
