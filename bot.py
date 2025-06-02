from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7670709310:AAEHgQkxcp4J30ZFBTXU9Z6mKUpp8q982Sg"  # токен вставлен

app = Flask(__name__)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает!")

# Telegram и обработчики
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))

# Ping-путь для Railway
@app.route("/")
def home():
    return "Bot is running!"

# Старт
if __name__ == "__main__":
    import asyncio
    async def main():
        await telegram_app.initialize()
        await telegram_app.start()
    asyncio.run(
