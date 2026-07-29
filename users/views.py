from rest_framework.generics import CreateAPIView

from users.models import User
from users.serializers import UserRegisterSerializer


class UserRegisterAPIView(CreateAPIView):
    """Регистрация пользователя."""

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
