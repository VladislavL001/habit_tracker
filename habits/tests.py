from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.test import APIRequestFactory, APITestCase

from habits.models import Habit
from habits.serializers import HabitSerializer
from users.models import User


class HabitSerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@mail.ru", password="12345678")

    def test_reward_and_related_habit_cannot_exist_together(self):
        pleasant_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="08:00",
            action="Выпить воды",
            is_pleasant=True,
            periodicity=1,
            execution_time=30,
        )

        data = {
            "place": "Дом",
            "time": "09:00",
            "action": "Почитать книгу",
            "is_pleasant": False,
            "reward": "Кофе",
            "related_habit": pleasant_habit.id,
            "periodicity": 1,
            "execution_time": 30,
        }

        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = self.user

        serializer = HabitSerializer(
            data=data,
            context={"request": request},
        )

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_pleasant_habit_cannot_have_reward(self):
        data = {
            "place": "Дом",
            "time": "09:00",
            "action": "Улыбнуться",
            "is_pleasant": True,
            "reward": "Шоколадка",
            "periodicity": 1,
            "execution_time": 30,
        }

        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = self.user

        serializer = HabitSerializer(
            data=data,
            context={"request": request},
        )

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class HabitAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@mail.ru", password="12345678")

        self.client.force_authenticate(user=self.user)

        self.second_user = User.objects.create_user(
            email="user2@mail.ru",
            password="12345678",
        )

    def test_create_habit(self):
        data = {
            "place": "Дом",
            "time": "08:00",
            "action": "Выпить воды",
            "is_pleasant": False,
            "reward": "Кофе",
            "periodicity": 1,
            "execution_time": 30,
            "is_public": False,
        }

        response = self.client.post(
            reverse("habit-list"),
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first().owner, self.user)
        self.assertEqual(Habit.objects.first().action, "Выпить воды")

    def test_user_cannot_update_foreign_habit(self):
        habit = Habit.objects.create(
            owner=self.second_user,
            place="Дом",
            time="08:00",
            action="Читать книгу",
            is_pleasant=False,
            reward="Кофе",
            periodicity=1,
            execution_time=30,
            is_public=False,
        )

        response = self.client.patch(
            reverse("habit-detail", args=[habit.id]),
            {"action": "Новое действие"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_sees_only_own_habits(self):
        Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="08:00",
            action="Моя привычка",
            is_pleasant=False,
            reward="Кофе",
            periodicity=1,
            execution_time=30,
            is_public=False,
        )

        Habit.objects.create(
            owner=self.second_user,
            place="Улица",
            time="09:00",
            action="Чужая привычка",
            is_pleasant=False,
            reward="Чай",
            periodicity=1,
            execution_time=30,
            is_public=False,
        )

        response = self.client.get(reverse("habit-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Моя привычка")

    def test_public_habits_list(self):
        Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="08:00",
            action="Публичная привычка",
            is_pleasant=False,
            reward="Кофе",
            periodicity=1,
            execution_time=30,
            is_public=True,
        )

        Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="09:00",
            action="Приватная привычка",
            is_pleasant=False,
            reward="Чай",
            periodicity=1,
            execution_time=30,
            is_public=False,
        )

        response = self.client.get(reverse("public-habits"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["action"],
            "Публичная привычка",
        )
