from rest_framework import serializers

from .models import Habit
from .validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, attrs):
        HabitValidator()(attrs, self)
        return attrs
