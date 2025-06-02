from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Flask(__name__)
BOT_TOKEN = "7670709310:AAEHgQk..."

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает. Привет!")

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ Доступные команды:\n/start — запустить бота\n/help — помощь")

# Проверка Railway
@app.route("/")
def home():
    return "Bot is running!"

# Запуск
if __name__ == "__main__":
    import asyncio

    async def main():
        application = ApplicationBuilder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))

        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        await application.updater.idle()

    asyncio.run(main())
