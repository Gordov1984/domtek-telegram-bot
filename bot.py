import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from docx import Document
import fitz  # PyMuPDF
import pandas as pd

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот-помощник. Пришли мне PDF, DOCX, TXT, XLSX, фото или видео — и я их обработаю.")

# PDF
async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_path = f"{file.file_unique_id}.pdf"
    await file.download_to_drive(file_path)

    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        preview = text[:4000] or "Файл пустой."
        await update.message.reply_text(f"Текст из PDF:\n\n{preview}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка PDF: {e}")
    finally:
        os.remove(file_path)

# DOCX
async def handle_docx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_path = f"{file.file_unique_id}.docx"
    await file.download_to_drive(file_path)

    try:
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        preview = text[:4000] or "Файл пустой."
        await update.message.reply_text(f"Текст из DOCX:\n\n{preview}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка DOCX: {e}")
    finally:
        os.remove(file_path)

# TXT
async def handle_txt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_path = f"{file.file_unique_id}.txt"
    await file.download_to_drive(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        preview = content[:4000] or "Файл пустой."
        await update.message.reply_text(f"Текст из TXT:\n\n{preview}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка TXT: {e}")
    finally:
        os.remove(file_path)

# XLSX
async def handle_xlsx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_path = f"{file.file_unique_id}.xlsx"
    await file.download_to_drive(file_path)

    try:
        df = pd.read_excel(file_path)
        preview = df.head().to_string()
        await update.message.reply_text(f"Таблица из XLSX:\n\n{preview}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка XLSX: {e}")
    finally:
        os.remove(file_path)

# Photo
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото получено! (Обработка изображений будет добавлена позже)")

# Video
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Видео получено! (Обработка видео пока отключена)")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.FILE_EXTENSION("pdf"), handle_pdf))
    app.add_handler(MessageHandler(filters.Document.FILE_EXTENSION("docx"), handle_docx))
    app.add_handler(MessageHandler(filters.Document.FILE_EXTENSION("txt"), handle_txt))
    app.add_handler(MessageHandler(filters.Document.FILE_EXTENSION("xlsx"), handle_xlsx))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))

    app.run_polling()

if __name__ == "__main__":
    main()
