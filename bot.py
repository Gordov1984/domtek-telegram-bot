from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"  # не забудь, в Railway он берётся из переменной окружения

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["/help", "/info"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Бот успешно запущен!", reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Доступные команды:\n/start – запустить бота\n/help – список команд\n/info – информация")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Это телеграм-бот ДомТек Ассистент 🤖")

def main():
    import os
    app = Application.builder().token(os.environ["BOT_TOKEN"]).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info))

    app.run_polling()
