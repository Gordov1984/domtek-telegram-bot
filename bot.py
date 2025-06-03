import logging
import os
import openai
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

# Настройка логов
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Токены и URL из переменных среды
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Установим ключ OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Ошибка в обработке сообщения: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуйте позже.")

# Запуск бота
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск через Webhook
    await app.run_webhook(
        listen="0.0.0.0",
        port=8000,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
