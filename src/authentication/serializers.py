from rest_framework import serializers

from shared.validators import user_password_validator, user_username_validator


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[user_username_validator])
    password = serializers.CharField(validators=[user_password_validator])
