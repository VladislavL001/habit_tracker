from rest_framework.pagination import LimitOffsetPagination


class HabitPagination(LimitOffsetPagination):
    """Пагинация для списка привычек."""

    default_limit = 5
    max_limit = 20