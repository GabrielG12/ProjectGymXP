from rest_framework import serializers
from exercises.models import Exercises
from .models import Training


class TrainingCreateSerializer(serializers.ModelSerializer):
    exercise = serializers.SlugRelatedField(queryset=Exercises.objects.all(), slug_field='name')
    username = serializers.CharField()

    class Meta:
        model = Training
        fields = ['id', 'exercise', 'type', 'username', 'quantity', 'date']
        read_only_fields = ['username', 'date']

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as e:
            errors = {}
            for field, value in e.detail.items():
                if field == 'exercise' and 'Object with name=' in value[0]:
                    errors[field] = "Exercise not found for the specified username."
                else:
                    errors[field] = value
            raise serializers.ValidationError(errors)

    def create(self, validated_data):
        exercise_name = validated_data['exercise']
        quantity = validated_data['quantity']
        type = validated_data['type']
        username = validated_data['username']
        exercise = Exercises.objects.filter(name=exercise_name, username=username).first()
        if exercise is None:
            raise serializers.ValidationError("Exercise not found for the specified username.")
        return Training.objects.create(username=username, exercise=exercise, quantity=quantity, type=type)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['username'] = instance.username.username
        return representation


class TrainingUserListSerializer(serializers.ModelSerializer):
    exercise = serializers.SlugRelatedField(queryset=Exercises.objects.all(), slug_field='name')
    username = serializers.CharField()

    class Meta:
        model = Training
        fields = ['id', 'exercise', 'type', 'username', 'quantity', 'date']


class TrainingDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = Training
        fields = ['id', 'username']


class TrainingUserUpdateSerializer(serializers.ModelSerializer):
    exercise = serializers.SlugRelatedField(queryset=Exercises.objects.all(), slug_field='name')
    username = serializers.CharField()

    class Meta:
        model = Training
        fields = '__all__'

