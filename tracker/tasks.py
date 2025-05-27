from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from tracker.models import Tracker
import telegram


@shared_task
def check_and_send_habit_reminders():
    """Простая задача для напоминаний о привычках"""
    habits = Tracker.objects.filter(
        next_reminder__lte=timezone.now(),
        is_active=True,
        user__telegram_chat_id__isnull=False
    )

    bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)

    for habit in habits:
        # Формируем сообщение
        message = f"🔔 Привычка: {habit.action}\nМесто: {habit.place}"

        bot.send_message(
            chat_id=habit.user.telegram_chat_id,
            text=message
        )

        habit.next_reminder = timezone.now() + timedelta(days=habit.periodicity)
        habit.save()
