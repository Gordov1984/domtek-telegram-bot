from telegram import Update, Document
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler
import os
import fitz  # PyMuPDF
import docx
import pandas as pd
from PIL import Image
import pytesseract

TOKEN = "твой_токен_сюда"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Пришли мне PDF, Word, Excel или фото, и я обработаю их.")

async def handle_doc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    file_name = document.file_name.lower()

    file = await context.bot.get_file(document.file_id)
    file_path = f"/tmp/{document.file_name}"
    await file.download_to_drive(file_path)

    response = ""

    try:
        if file_name.endswith('.pdf'):
            doc = fitz.open(file_path)
            for page in doc:
                response += page.get_text()
            doc.close()
            response = response.strip() or "PDF пустой или нечитабельный."

        elif file_name.endswith('.docx'):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                response += para.text + '\n'
            response = response.strip() or "Документ пустой."

        elif file_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
            response = df.to_string(index=False)
            response = response.strip() or "Файл Excel пустой или нечитабельный."

        else:
            response = "Тип файла не поддерживается."

    except Exception as e:
        response = f"Ошибка: {e}"

    await update.message.reply_text(response[:4000])  # Telegram лимит

    os.remove(file_path)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = "/tmp/photo.jpg"
    await file.download_to_drive(file_path)

    try:
        text = pytesseract.image_to_string(Image.open(file_path))
        text = text.strip() or "Текст не найден."
        await update.message.reply_text(text[:4000])
    except Exception as e:
        await update.message.reply_text(f"Ошибка при обработке фото: {e}")
    finally:
        os.remove(file_path)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_doc))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()

if __name__ == "__main__":
    main()
