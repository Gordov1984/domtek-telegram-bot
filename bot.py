import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai
from aiohttp import web

# 🔐 Переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне текст или документ, и я всё оформлю.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        await update.message.reply_text("Отправь текстовое сообщение.")
        return
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}]
    )
    await update.message.reply_text(response['choices'][0]['message']['content'])

# 🔁 Webhook endpoint
async def webhook_view(request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return web.Response()

# ⚙️ Инициализация приложения
application = Application.builder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

async def main():
    # Обязательная инициализация для webhook
    await application.initialize()

    # Установка webhook
    await application.bot.set_webhook(url=WEBHOOK_URL)

    # Запуск сервера
    app = web.Application()
    app.router.add_post("/", webhook_view)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

    logging.info("🚀 Бот запущен на webhook!")

    await application.start()
    await application.updater.start_polling()  # Можно закомментить, если чисто webhook

    # Ожидание остановки
    await application.updater.wait()
    await application.stop()
    await application.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
