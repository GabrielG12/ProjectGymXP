from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from .models import Exercises
from rest_framework.exceptions import APIException

User = get_user_model()
class UnauthorizedException(APIException):
    status_code = 403
    default_detail = "You are not authorized to perform this action."

class ExercisesCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Exercises
        fields = ['name', 'exercise_type', 'username']

    def create(self, validated_data):
        username = validated_data['user']['username']
        user = User.objects.get(username=username)
        if user != self.context['request'].user:
            raise UnauthorizedException()
        exercise_type = validated_data['exercise_type']
        name = validated_data['name']
        exercise = Exercises.objects.create(username=user, name=name, exercise_type=exercise_type)
        return exercise


class ExercisesUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = ['id', 'name', 'exercise_type', 'username']


class ExercisesDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = ['name', 'username']


class ExercisesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercises
        fields = ['name', 'exercise_type', 'username']