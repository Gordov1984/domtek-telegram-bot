from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os
import asyncio

# Init
TOKEN = os.environ["BOT_TOKEN"]
app = Flask(__name__)

# Telegram application
application = Application.builder().token(TOKEN).build()

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я @domtek_assistant_bot.")

# Обработка обычных сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Вы сказали: {update.message.text}")

# Обработка ошибок
async def error_handler(update, context):
    print(f"Произошла ошибка: {context.error}")

# Хендлеры
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
application.add_error_handler(error_handler)

# Flask endpoint для Telegram webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"

# Health-check (Render пингует сюда)
@app.route("/healthz", methods=["GET"])
def health_check():
    return "ok"

if __name__ == "__main__":
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=f"https://domtek-telegram-bot.onrender.com/{TOKEN}"
    )
