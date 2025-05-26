import telegram
from celery import shared_task
from django.conf import settings


@shared_task
def send_telegram_reminder(chat_id: int, message: str):
    """Базовая задача для отправки сообщения в Telegram"""
    if not chat_id:
        return

    bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
    bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode='Markdown'
    )
