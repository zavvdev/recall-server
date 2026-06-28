from django.contrib.auth import get_user_model
from rest_framework import serializers, status

from shared.constants import USER_NAME_MAX_LEN
from shared.exceptions import AppException
from shared.messages import Messages
from shared.validators import user_password_validator, user_username_validator


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[user_username_validator])
    email = serializers.EmailField()
    # write_only=True allows us to exclude this field from being send back in
    # the response, so we don't expose hashed password.
    password = serializers.CharField(
        write_only=True, validators=[user_password_validator]
    )
    name = serializers.CharField(max_length=USER_NAME_MAX_LEN)

    # This method is called automatically when we call serializer.is_valid().
    def validate(self, attrs):
        User = get_user_model()
        if (
            User.objects.filter(username=attrs["username"]).exists()
            or User.objects.filter(email=attrs["email"]).exists()
        ):
            raise AppException(
                status_code=status.HTTP_409_CONFLICT,
                message=Messages.AUTH_USER_CREATION_FAILED,
            )
        return attrs

    # This method is called automatically when we call serializer.save().
    # It uses validated data so we don't need to do the creation process
    # manually.
    # We can also create an "update" method which is called when we connect
    # a model to serializer like this:
    # serializer = UserSerializer(instance=user, data=request.data)
    # so when we call serializer.save() it calls "update" instead of "create".
    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[user_username_validator])
    password = serializers.CharField(validators=[user_password_validator])
