from rest_framework.serializers import ValidationError


class HabitValidator:
    """Валидатор привычек."""

    def __call__(self, attrs, serializer):
        instance = serializer.instance

        is_pleasant = attrs.get(
            "is_pleasant",
            instance.is_pleasant if instance else False,
        )

        reward = attrs.get(
            "reward",
            instance.reward if instance else None,
        )

        related_habit = attrs.get(
            "related_habit",
            instance.related_habit if instance else None,
        )

        execution_time = attrs.get(
            "execution_time",
            instance.execution_time if instance else 0,
        )

        periodicity = attrs.get(
            "periodicity",
            instance.periodicity if instance else 1,
        )

        # 1. Нельзя одновременно указывать вознаграждение и связанную привычку
        if reward and related_habit:
            raise ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )

        # 2. Время выполнения
        if execution_time > 120:
            raise ValidationError(
                "Время выполнения привычки не должно превышать 120 секунд."
            )

        # 3. Приятная привычка
        if is_pleasant and (reward or related_habit):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        # 4. Связанная привычка должна быть приятной
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        # 5. Периодичность
        if periodicity > 7:
            raise ValidationError(
                "Нельзя выполнять привычку реже одного раза в 7 дней."
            )
