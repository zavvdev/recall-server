from enum import StrEnum

from django.conf import settings
from django.db import models
from django.db.models import Q

from shared.models import ModelBase, Visibility


class ProfileLang(StrEnum):
    EN = "en"


class ProfileTheme(StrEnum):
    DARK = "dark"
    LIGHT = "light"


class UserProfile(ModelBase):
    # Create one-to-one relationship between user and profile.
    # Field has name "user", not user_id or profile_user.
    # Django automatically creates the underlying database column
    # user_id, while out Python code accesses it as profile.user
    user = models.OneToOneField(
        # We use this instead of directly importing User model.
        # This works whether we’re using Django’s built-in user
        # model or a custom one.
        settings.AUTH_USER_MODEL,
        # If associated user model gets deleted, then its profile
        # is deleted automatically.
        on_delete=models.CASCADE,
        # Name of the field that is used to access profile from user:
        # "user.profile".
        related_name="profile",
    )

    visibility = models.CharField(
        max_length=10,
        # First value from tuple is being used by Django for validation.
        # The second one is just a label. We could use v.name.
        choices=[(v.value, v.value) for v in Visibility],
        default=Visibility.PRIVATE,
    )

    language = models.CharField(
        max_length=3,
        choices=[(v.value, v.value) for v in ProfileLang],
        default=ProfileLang.EN,
    )

    theme = models.CharField(
        max_length=5,
        choices=[(v.value, v.value) for v in ProfileTheme],
        default=ProfileTheme.LIGHT,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(visibility__in=[v.value for v in Visibility]),
                name="visibility_valid",
            ),
            models.CheckConstraint(
                condition=Q(language__in=[v.value for v in ProfileLang]),
                name="language_valid",
            ),
            models.CheckConstraint(
                condition=Q(theme__in=[v.value for v in ProfileTheme]),
                name="theme_valid",
            ),
        ]
