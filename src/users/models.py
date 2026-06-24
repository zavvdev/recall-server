from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Q

from shared.constants import USER_NAME_MAX_LEN, USER_USERNAME_MAX_LEN
from shared.models import ModelBase
from shared.validators import user_username_validator


# Manager is a layer between a model and the database query logic.
# You write your own manager when you want to add custom query logic
# for your modal that you don't want to duplicate.
#
# AbstractBaseUser requires a manager to tell Django how to create users —
# specifically how to handle password hashing. Without it we'd have to call
# set_password() manually every time you create a user.
# It also normalizes the email (lowercases the domain part e.g.
# User@GMAIL.COM → User@gmail.com) so we don't get duplicate accounts from
# the same email with different casing.
#
# AbstractUser — batteries included. Good when we mostly like Django's default
# user and just want to tweak a few things.
# AbstractBaseUser — bare minimum. Just password hashing and auth primitives.
# You define everything else yourself. More work upfront but a clean model
# with no baggage.
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        # Normalize email before lookup in DB so that varying case
        # in the domain doesn't block authentication.
        #
        # ** unpacks dictionary into key=value args;
        # kwargs = {"email": email}
        # self.get(**kwargs)
        # becomes self.get(email=email)
        email = self.normalize_email(username)
        return self.get(**{self.model.USERNAME_FIELD: email})


# This model needs to be assigned to AUTH_USER_MODEL variable inside
# config/settings/base.py since we overriding default Django model for
# authentication. It has to be done before running migration.
class User(AbstractBaseUser, ModelBase):
    # These fields are required since we didn't specify
    # blank=True or null=True
    #
    # null
    # If True, Django will store empty values as NULL in the database.
    # Default is False.
    #
    # blank
    # If True, the field is allowed to be blank. Default is False.
    # Note that this is different than null. null is purely
    # database-related, whereas blank is validation-related. If a field
    # has blank=True, form validation will allow entry of an empty value.
    # If a field has blank=False, the field will be required.

    username = models.CharField(
        unique=True,
        max_length=USER_USERNAME_MAX_LEN,
        validators=[user_username_validator],
    )
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=USER_NAME_MAX_LEN)

    # Remove last_login field that is inherited from AbstractBaseUser model.
    last_login = None

    # Password is already provided by AbstractBaseUser as well as its hashing.

    # A string describing the name of the field on the user model that is
    # used as the unique identifier. This will usually be a username of
    # some kind, but it can also be an email address, or any other unique
    # identifier. The field must be unique (e.g. have unique=True set in
    # its definition), unless you use a custom authentication backend that
    # can support non-unique usernames. We still need to provide USERNAME_FIELD
    # even if we add our custom authentication backend for handling fields
    # which can be used for authentication.
    USERNAME_FIELD = "email"

    # A list of the field names that will be prompted for when creating
    # a user via the createsuperuser management command. The user will be
    # prompted to supply a value for each of these fields. It must include
    # any field for which blank is False or undefined and may include
    # additional fields you want prompted for when a user is created
    # interactively. REQUIRED_FIELDS has no effect in other parts of Django,
    # like creating a user in the admin. So, we're leaving this field empty
    # since we don't need admin app. But it still needs to be included
    # because otherwise it will be pulled from default AbstractBaseUser
    # implementation and will cause an error.
    REQUIRED_FIELDS = []

    # Do not rename it since internal auth logic expects this name.
    objects = UserManager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                # Disallow using @ in usernames at the database level.
                condition=~Q(username__contains="@"),
                name="users_user_username_no_at_sign",
            )
        ]

    def __str__(self):
        return self.email
