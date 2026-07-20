from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from habits.models import Habit
from habits.pagination import HabitPagination
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitPagination

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "is_pleasant",
        "is_public",
        "periodicity",
    ]

    def get_queryset(self):
        if self.action == "list":
            return Habit.objects.filter(owner=self.request.user)

        return Habit.objects.all()


class PublicHabitListAPIView(generics.ListAPIView):
    """Список публичных привычек."""

    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    pagination_class = HabitPagination
    queryset = Habit.objects.filter(is_public=True)
