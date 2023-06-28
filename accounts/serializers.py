from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import User
from rest_framework.authtoken.models import Token


class SignUpSerializer(serializers.ModelSerializer):

    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    #TODO: PASSWORD NI VIDEN NOBENEMU Z write_only =TRUE
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    #TODO: POGLEDAMO ČE USRERNAME IN EMAIL ŽE OBSTAJATA V BAZI
    def validate(self, attrs):
        username_exists = User.objects.filter(username=attrs['username']).exists()
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if username_exists:
            raise ValidationError("Username already exists. Try using new username!")
        if email_exists:
            raise ValidationError("Email already exists. Try using new email!")
        return super().validate(attrs)

    #TODO: HASHIRAMO USERJA DA ADMIN NE VIDI PASSWORDA
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user


class CurrentUserExercisesSerializer(serializers.ModelSerializer):

    exercises = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'exercises']
