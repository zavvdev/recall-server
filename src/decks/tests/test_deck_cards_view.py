from django.urls import reverse
from rest_framework import status

from cards.models import CardKind
from shared.messages import Messages
from shared.tests.base import BaseAPITestCase
from shared.url_names import UrlName


class DeckCardsViewTest(BaseAPITestCase):
    def test_get_retrieves_cards_by_deck_id(self):
        self.login()
        create_deck_res = self.client.post(
            reverse(UrlName.DECK_LIST),
            {
                "name": "Test deck",
            },
        )
        self.client.post(
            reverse(UrlName.CARD),
            {
                "kind": CardKind.BASIC,
                "front": "1",
                "back": "2",
                "deck": create_deck_res.data["data"]["id"],
            },
        )
        get_res = self.client.get(
            reverse(
                UrlName.DECK_CARDS,
                kwargs={"pk": create_deck_res.data["data"]["id"]},
            ),
        )
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(get_res.data["data"]), 1)

    def test_get_returns_404_if_deck_not_found(self):
        self.login()
        get_res = self.client.get(
            reverse(
                UrlName.DECK_CARDS,
                kwargs={"pk": "869afa86-3f70-402e-9963-34a12a729ccd"},
            ),
        )
        self.assertEqual(get_res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get_res.data["message"], Messages.DECK_NOT_FOUND)

    def test_get_returns_404_if_deck_belongs_to_other_user(self):
        self.register_user(username="other")
        self.login_user(username="other")
        create_deck_res = self.client.post(
            reverse(UrlName.DECK_LIST),
            {
                "name": "Test deck",
            },
        )
        self.client.post(
            reverse(UrlName.CARD),
            {
                "kind": CardKind.BASIC,
                "front": "1",
                "back": "2",
                "deck": create_deck_res.data["data"]["id"],
            },
        )
        self.login()
        get_res = self.client.get(
            reverse(
                UrlName.DECK_CARDS,
                kwargs={"pk": create_deck_res.data["data"]["id"]},
            ),
        )
        self.assertEqual(get_res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get_res.data["message"], Messages.DECK_NOT_FOUND)
