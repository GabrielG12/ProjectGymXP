from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Exercises



User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ExercisesSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Exercises
        fields = ['name', 'type', 'username']

    def create(self, validated_data):
        user = self.context['request'].user
        exercise = Exercises.objects.create(
            username=user,
            type=validated_data['type'],
            name=validated_data['name']
        )
        return exercise
