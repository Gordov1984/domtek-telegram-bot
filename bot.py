import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
from python_docx import Document  # Используем python-docx

# Замените на свой токен
BOT_TOKEN = os.getenv("BOT_TOKEN", "вставь_сюда_токен")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-помощник.\n"
        "Отправь мне файл (PDF, DOCX, изображение), и я помогу!"
    )

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — запустить бота\n"
        "/help — список команд"
    )

# Обработка документов
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if file is None:
        return

    file_id = file.file_id
    file_name = file.file_name
    new_file = await context.bot.get_file(file_id)
    await update.message.chat.send_action(action=ChatAction.TYPING)
    await new_file.download_to_drive(f"./{file_name}")

    await update.message.reply_text(
        f"Файл '{file_name}' получен!\nОбрабатываю..."
    )

    # Симуляция анализа
    await update.message.reply_text("✅ Анализ файла завершён (симуляция).")

# Обработка изображений
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Картинка получена! Обрабатываю (симуляция)...")
    await update.message.reply_text("✅ Анализ изображения завершён (симуляция).")

# Роут для Railway
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Регистрация хендлеров
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.Document.ALL, handle_file))
application.add_handler(MessageHandler(filters.PHOTO, handle_image))

# Запуск локального режима (если нужно)
if __name__ == "__main__":
    application.run_polling()
