from enum import StrEnum


# Messages for api responses.
class Messages(StrEnum):
    # common
    OK = "ok"
    UNEXPECTED_ERROR = "unexpected_error"
    VALIDATION_ERROR = "validation_error"
    INVALID = "invalid"
    NOT_FOUND = "not_found"
    PERMISSION_DENIED = "permission_denied"
    NOT_AUTHENTICATED = "not_authenticated"
    REQUIRED = "required"
    TOO_LONG = "too_long"
    TOO_SHORT = "too_short"

    # authentication
    AUTH_INVALID_CREDENTIALS = "auth_invalid_credentials"
    AUTH_USER_CREATION_FAILED = "auth_user_creation_failed"
