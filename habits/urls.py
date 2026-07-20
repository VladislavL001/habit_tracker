from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.views import HabitViewSet, PublicHabitListAPIView

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")

urlpatterns = [
    path(
        "public-habits/",
        PublicHabitListAPIView.as_view(),
        name="public-habits",
    ),
]

urlpatterns += router.urls
