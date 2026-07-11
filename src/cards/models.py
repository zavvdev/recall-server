from enum import StrEnum

from django.db import models
from django.db.models import Q

from decks.models import Deck
from shared.constants import CARD_KIND_MAX_LEN, CARD_TEXT_MAX_LEN
from shared.constraints import ConstraintName
from shared.models import ModelBase


class CardKind(StrEnum):
    BASIC = "basic"
    REVERSE = "reverse"


class Card(ModelBase):
    # Deck can have multiple cards, one card can be
    # related to only one deck at a time.
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
        related_name="cards",
    )

    kind = models.CharField(
        max_length=CARD_KIND_MAX_LEN,
        choices=[(v.value, v.value) for v in CardKind],
        default=CardKind.BASIC,
    )

    front = models.CharField(
        max_length=CARD_TEXT_MAX_LEN,
    )

    back = models.CharField(
        max_length=CARD_TEXT_MAX_LEN,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(kind__in=[v.value for v in CardKind]),
                name=ConstraintName.CARD_KIND_VALID,
            ),
        ]
