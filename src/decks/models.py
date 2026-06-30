from django.conf import settings
from django.db import models
from django.db.models import Q

from shared.constants import DECK_NAME_MAX_LEN, VISIBILITY_MAX_LEN
from shared.constraints import ConstraintName
from shared.models import ModelBase, Visibility


class Deck(ModelBase):
    # Create one-to-one relationship between user and deck.
    # Field has name "user", not user_id. Django automatically
    # creates the underlying database column user_id, while our
    # Python code accesses it as deck.user
    user = models.OneToOneField(
        # We use this instead of directly importing User model.
        # This works whether we’re using Django’s built-in user
        # model or a custom one.
        settings.AUTH_USER_MODEL,
        # If associated user model gets deleted, then deck
        # is deleted automatically.
        on_delete=models.CASCADE,
        # Name of the field that is used to access deck from user:
        # "user.deck".
        related_name="deck",
    )

    name = models.CharField(max_length=DECK_NAME_MAX_LEN)

    visibility = models.CharField(
        max_length=VISIBILITY_MAX_LEN,
        # First value from tuple is being used by Django for validation.
        # The second one is just a label. We could use v.name.
        choices=[(v.value, v.value) for v in Visibility],
        default=Visibility.PRIVATE,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(visibility__in=[v.value for v in Visibility]),
                name=ConstraintName.DECK_VISIBILITY_VALID,
            ),
        ]
