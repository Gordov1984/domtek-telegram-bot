from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

app = Flask(__name__)

# ВСТАВЬ СЮДА СВОЙ БОТ ТОКЕН в кавычках
BOT_TOKEN = "7670709310:AAEHgQkxcp4J30ZFBTXU9Z6mKUpp8q982Sg"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает!")

# Пинг от Railway
@app.route("/")
def home():
    return "Bot is running!"

# Запуск Telegram-бота
if __name__ == "__main__":
    async def main():
        telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
        telegram_app.add_handler(CommandHandler("start", start))
        await telegram_app.initialize()
        await telegram_app.start()
        await telegram_app.updater.start_polling()
        await telegram_app.updater.idle()

    asyncio.run(main())
