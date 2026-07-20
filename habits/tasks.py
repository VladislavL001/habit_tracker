from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from telegram_bot.services import send_telegram_message


@shared_task
def send_habit_reminders():
    """Отправляет напоминания о привычках."""

    current_time = timezone.localtime().time().replace(second=0, microsecond=0)

    habits = Habit.objects.filter(
        time=current_time,
        owner__telegram_chat_id__isnull=False,
    ).exclude(owner__telegram_chat_id="")

    for habit in habits:
        send_telegram_message(
            chat_id=habit.owner.telegram_chat_id,
            text=f"⏰ Пора выполнить привычку: {habit.action}",
        )
