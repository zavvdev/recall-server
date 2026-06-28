"""
Model serializer has two primary modes:

1.  Read mode (Serialization) -- Converts a model instance into
    primitive Python types that can be rendered as JSON.

2.  Write mode (Deserialization)** -- Validates incoming request data
    and optionally creates or updates model instances.

The mode is determined by the arguments passed to the serializer
constructor.

Read Mode

Convert an existing model instance into a JSON-compatible
representation.

serializer = UserProfileSerializer(profile)

Input: Model instance
Output: serializer.data

No validation occurs in this mode.

Write Mode (Create)

serializer = UserProfileSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
serializer.save()

Uses the automatically generated `create()` method.

Write Mode (Update)

serializer = UserProfileSerializer(profile, data=request.data)
serializer.is_valid(raise_exception=True)
serializer.save()

Passing an existing instance tells DRF to call `update()` instead of
`create()`. `ModelSerializer` already provides a default implementation.

Partial Update

serializer = UserProfileSerializer(
    profile,
    data=request.data,
    partial=True,
)

Only supplied fields are validated and updated.

We can re-define create/update methods if we need an additional logic
apart from simple create/update from model fields.
"""

from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        # Model that has to be passed into this serializer
        # in order to extract fields.
        model = UserProfile
        fields = ["visibility", "language", "theme"]
