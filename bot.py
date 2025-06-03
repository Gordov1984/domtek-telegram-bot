from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Привет! Бот работает.")

app = ApplicationBuilder().token("7670709310:AAEHgQkxcp4J30ZFBTXU9Z6mKUpp8q982Sg").build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
