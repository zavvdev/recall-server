from enum import StrEnum


class ConstraintName(StrEnum):
    USER_USERNAME_NO_AT_SIGN = "user_username_no_at_sign"

    PROFILE_VISIBILITY_VALID = "profile_visibility_valid"
    PROFILE_LANGUAGE_VALID = "profile_language_valid"
    PROFILE_THEME_VALID = "profile_theme_valid"

    DECK_VISIBILITY_VALID = "deck_visibility_valid"
