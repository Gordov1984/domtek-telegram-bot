import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Логи
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токены и ключи из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Хендлер сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

# Основной запуск
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Добавляем хендлер
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Устанавливаем webhook
    await app.initialize()
    await app.start()
    await app.bot.set_webhook(WEBHOOK_URL)
    await app.updater.start_webhook()
    print("Бот запущен через Webhook...")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
