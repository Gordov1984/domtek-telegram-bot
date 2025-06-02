import logging
from telegram import Update, Document
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ✅ Логирование
logging.basicConfig(level=logging.INFO)

# 🧠 Ответ на команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот-помощник. Отправь мне файл (PDF, DOCX, изображение), и я помогу!")

# 🧠 Ответ на команду /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Доступные команды:\n/start — запустить бота\n/help — список команд")

# 📥 Обработка входящих файлов
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    file_id = file.file_id
    new_file = await context.bot.get_file(file_id)
    file_path = f"received_{file.file_name}"
    await new_file.download_to_drive(file_path)

    await update.message.reply_text(f"Файл '{file.file_name}' получен! Обрабатываю...")

    # ⚠️ Тут в будущем будет отправка файла мне в OpenAI для анализа
    await update.message.reply_text(f"✅ Анализ файла завершён (симуляция).")

# 🖼️ Обработка изображений
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file_id = photo.file_id
    new_file = await context.bot.get_file(file_id)
    file_path = f"received_photo.jpg"
    await new_file.download_to_drive(file_path)

    await update.message.reply_text("Изображение получено! Обрабатываю...")
    # ⚠️ Тут будет анализ изображения
    await update.message.reply_text("✅ Анализ изображения завершён (симуляция).")

# 🚀 Основной запуск
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()

if __name__ == "__main__":
    main()
