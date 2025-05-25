import telegram
from celery import shared_task
from django.conf import settings
from datetime import timedelta
from tracker.models import Tracker


@shared_task
def send_telegram_reminder(chat_id: int, message: str):
    """Базовая задача для отправки сообщения в Telegram"""
    bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
    bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode='Markdown'  # Поддержка форматирования
    )


@shared_task
def check_and_send_reminders():
    """Периодическая проверка привычек для напоминаний"""
    from django.utils import timezone
    habits = Tracker.objects.filter(
        next_reminder__lte=timezone.now(),
        is_active=True  # Дополнительный флаг активности
    )

    for habit in habits:
        message = (
            f"🔔 *Напоминание о привычке*\n"
            f"Действие: {habit.action}\n"
            f"Место: {habit.place}\n"
            f"Время выполнения: {habit.duration} сек."
        )
        send_telegram_reminder.delay(
            chat_id=habit.user.tg_id_chat,
            message=message
        )
        # Обновляем время следующего напоминания
        habit.next_reminder = timezone.now() + timedelta(days=habit.periodicity)
        habit.save()
