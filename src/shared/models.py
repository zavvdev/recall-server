import uuid
from enum import StrEnum

from django.db import models


class Visibility(StrEnum):
    PRIVATE = "private"
    PUBLIC = "public"


# Base model that sets up some fields in order to not duplicate
# it for each model.
class ModelBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # This field will be set to now only once when record is created.
    created_at = models.DateTimeField(auto_now_add=True)
    # This will be updated every time when record is updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Abstract base classes are useful when you want to put some
        # common information into a number of other models. You write
        # your base class and put abstract=True in the Meta class.
        # This model will then not be used to create any database table.
        # Instead, when it is used as a base class for other models, its
        # fields will be added to those of the child class.
        abstract = True
