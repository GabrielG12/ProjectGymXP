from rest_framework import serializers
from exercises.models import Exercises
from .models import Training


class TrainingCreateSerializer(serializers.ModelSerializer):
    exercise = serializers.SlugRelatedField(queryset=Exercises.objects.all(), slug_field='name')
    username = serializers.CharField()
    repetitions = serializers.IntegerField(required=False)
    time_type = serializers.ChoiceField(choices=[('Seconds', 'Seconds'), ('Minutes', 'Minutes'), ('Hours', 'Hours')], required=False)

    class Meta:
        model = Training
        fields = ['id', 'username', 'exercise', 'quantity_type', 'quantity', 'repetitions', 'time_type', 'date']
        read_only_fields = ['username', 'date']

    def validate(self, attrs):
        quantity_type = attrs.get('quantity_type')
        repetitions = attrs.get('repetitions')
        time_type = attrs.get('time_type')

        if quantity_type == 'Sets' and repetitions is None:
            raise serializers.ValidationError("Repetitions is required when quantity_type is 'Sets'.")
        if quantity_type == 'Time' and time_type is None:
            raise serializers.ValidationError("Time type is required when quantity_type is 'Time'.")
        return attrs

    def create(self, validated_data):
        exercise_name = validated_data['exercise']
        quantity = validated_data['quantity']
        quantity_type = validated_data['quantity_type']
        repetitions = validated_data.get('repetitions')
        time_type = validated_data.get('time_type')
        username = validated_data['username']
        exercise = Exercises.objects.filter(name=exercise_name, username=username).first()
        if exercise is None:
            raise serializers.ValidationError("Exercise not found for the specified username.")
        training_data = {
            'username': username,
            'exercise': exercise,
            'quantity_type': quantity_type,
            'quantity': quantity,
        }
        if quantity_type == 'Sets':
            training_data['repetitions'] = repetitions
        elif quantity_type == 'Time':
            training_data['time_type'] = time_type
        return Training.objects.create(**training_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['username'] = instance.username.username
        return representation


class TrainingUserListSerializer(serializers.ModelSerializer):
    exercise = serializers.SlugRelatedField(queryset=Exercises.objects.all(), slug_field='name')
    username = serializers.CharField()

    class Meta:
        model = Training
        fields = ['id', 'username', 'exercise', 'quantity_type', 'quantity', 'repetitions', 'time_type', 'date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {key: value for key, value in representation.items() if value is not None and value != ''}


class TrainingUserRetrieveSerializer(serializers.ModelSerializer):
    exercise = serializers.SlugRelatedField(queryset=Exercises.objects.all(), slug_field='name')
    username = serializers.CharField()
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Training
        fields = ['id', 'username', 'exercise', 'quantity_type', 'quantity', 'repetitions', 'time_type', 'date']
        read_only = ['quantity_type', 'quantity']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {key: value for key, value in representation.items() if value is not None and value != ''}


class TrainingDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = Training
        fields = ['id', 'username']


class TrainingUserUpdateSerializer(serializers.ModelSerializer):
    exercise = serializers.SlugRelatedField(queryset=Exercises.objects.all(), slug_field='name')
    username = serializers.CharField()

    class Meta:
        model = Training
        fields = ['id', 'username', 'exercise', 'quantity_type', 'quantity', 'repetitions', 'time_type', 'date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {key: value for key, value in representation.items() if value is not None and value != ''}

