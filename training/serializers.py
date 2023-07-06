from rest_framework import serializers
from exercises.models import Exercises
from .models import Training


class TrainingCreateSerializer(serializers.ModelSerializer):
    exercise = serializers.SlugRelatedField(queryset=Exercises.objects.all(), slug_field='name')
    username = serializers.CharField()

    class Meta:
        model = Training
        fields = ['id', 'exercise', 'quantity_type', 'quantity', 'username', 'date']
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
        quantity_type = validated_data['quantity_type']
        username = validated_data['username']
        exercise = Exercises.objects.filter(name=exercise_name, username=username).first()
        if exercise is None:
            raise serializers.ValidationError("Exercise not found for the specified username.")
        return Training.objects.create(username=username, exercise=exercise, quantity_type=quantity_type, quantity=quantity)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['username'] = instance.username.username
        return representation


class TrainingUserListSerializer(serializers.ModelSerializer):
    exercise = serializers.SlugRelatedField(queryset=Exercises.objects.all(), slug_field='name')
    username = serializers.CharField()

    class Meta:
        model = Training
        fields = ['id', 'exercise', 'username', 'quantity_type', 'quantity', 'date']


class TrainingUserRetrieveSerializer(serializers.ModelSerializer):
    exercise = serializers.SlugRelatedField(queryset=Exercises.objects.all(), slug_field='name')
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Training
        fields = '__all__'
        read_only = ['quantity_type', 'quantity']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['username'] = instance.username.username
        return representation


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

