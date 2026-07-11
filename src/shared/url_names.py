from enum import StrEnum


class UrlName(StrEnum):
    AUTH_REGISTER = "auth_register"
    AUTH_LOGIN = "auth_login"
    AUTH_REFRESH = "auth_refresh"

    DECK_LIST = "deck_list"
    DECK_DETAIL = "deck_detail"
    DECK_CARDS = "deck_cards"

    USER_PROFILE = "user_profile"

    CARD = "card"
