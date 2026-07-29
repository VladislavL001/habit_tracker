from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from telegram_bot.services import send_telegram_message


@shared_task
def send_habit_reminders():
    """Отправляет напоминания о привычках."""

    now = timezone.localtime()
    current_time = now.time().replace(second=0, microsecond=0)
    today = now.date()

    habits = Habit.objects.filter(
        time=current_time,
        owner__telegram_chat_id__isnull=False,
    ).exclude(owner__telegram_chat_id="")

    for habit in habits:
        if (
            habit.last_notification is None
            or (today - habit.last_notification).days >= habit.periodicity
        ):
            send_telegram_message(
                chat_id=habit.owner.telegram_chat_id,
                text=f"⏰ Пора выполнить привычку: {habit.action}",
            )

            habit.last_notification = today
            habit.save(update_fields=["last_notification"])
