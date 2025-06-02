from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Flask(__name__)

# Вставь свой токен ниже вместо YOUR_BOT_TOKEN
BOT_TOKEN = "YOUR_BOT_TOKEN"

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает! Всё хорошо.")

# Инициализация телеграм-бота
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))

# Ping для Railway
@app.route("/")
def home():
    return "Bot is running!"

# Запуск polling
if __name__ == "__main__":
    import asyncio
    async def main():
        await telegram_app.initialize()
        await telegram_app.start()
        await telegram_app.updater.start_polling()
    asyncio.run(main())
