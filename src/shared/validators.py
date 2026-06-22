from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import RegexValidator, validate_email

user_password_validator = RegexValidator(
    regex=r"^.{8,}$",
)


def user_username_validator(value):
    # try email first
    try:
        validate_email(value)
        return value
    except DjangoValidationError:
        pass

    # fallback to username rules
    RegexValidator(regex=r"^[a-zA-Z_][a-zA-Z0-9_]*$")(value)
    return value
