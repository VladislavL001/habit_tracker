import os

import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))


def send_telegram_message(chat_id: int, text: str) -> None:
    """Отправляет сообщение пользователю в Telegram."""
    bot.send_message(chat_id=chat_id, text=text)
