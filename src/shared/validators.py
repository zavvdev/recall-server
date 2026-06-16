from django.core.validators import RegexValidator

user_username_validator = RegexValidator(regex=r"^[a-zA-Z_][a-zA-Z0-9_]*$")

user_password_validator = RegexValidator(
    regex=r"^.{8,}$",
)
