import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from docx import Document
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# === Команды ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот-помощник.\nОтправь мне файл (PDF, DOCX, изображение), и я помогу!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Доступные команды:\n/start — запустить бота\n/help — список команд")

# === Обработка текстовых документов ===
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    file_name = file.file_name.lower()
    file_id = file.file_id
    new_file = await context.bot.get_file(file_id)
    file_bytes = await new_file.download_as_bytearray()

    await update.message.reply_text(f"Файл '{file.file_name}' получен!\nОбрабатываю...")

    try:
        if file_name.endswith(".docx"):
            doc = Document(BytesIO(file_bytes))
            text = "\n".join([p.text for p in doc.paragraphs])
        elif file_name.endswith(".pdf"):
            text = ""
            with fitz.open(stream=file_bytes, filetype="pdf") as pdf:
                for page in pdf:
                    text += page.get_text()
        elif file_name.endswith((".jpg", ".jpeg", ".png", ".webp")):
            image = Image.open(BytesIO(file_bytes))
            text = "[Изображение получено. Распознавание текста пока не подключено.]"
        else:
            await update.message.reply_text("⚠️ Неподдерживаемый формат файла.")
            return

        if not text.strip():
            text = "⚠️ Текст не найден или файл пуст."

        await update.message.reply_text(f"✅ Анализ завершён:\n\n{text[:3500]}")  # Telegram ограничение ~4096

    except Exception as e:
        logging.error(f"Ошибка при обработке файла: {e}")
        await update.message.reply_text("❌ Произошла ошибка при обработке файла.")

# === Основной запуск ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    app.run_polling()

if __name__ == "__main__":
    main()
