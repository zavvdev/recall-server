from django.urls import reverse
from rest_framework import status

from cards.models import CardKind
from shared.messages import Messages
from shared.tests.base import BaseAPITestCase
from shared.url_names import UrlName


class CardListViewTest(BaseAPITestCase):
    def test_post_creates_new_card(self):
        self.login()
        create_deck_res = self.client.post(
            reverse(UrlName.DECK_LIST),
            {
                "name": "Test deck",
            },
        )
        self.client.post(
            reverse(UrlName.CARD_LIST),
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
        self.assertEqual(get_res.data["data"][0]["front"], "1")
        self.assertEqual(get_res.data["data"][0]["back"], "2")
        self.assertEqual(get_res.data["data"][0]["kind"], CardKind.BASIC)

    def test_post_returns_400_if_deck_not_found(self):
        self.login()
        res = self.client.post(
            reverse(UrlName.CARD_LIST),
            {
                "kind": CardKind.BASIC,
                "front": "1",
                "back": "2",
                "deck": "869afa86-3f70-402e-9963-34a12a729ccd",
            },
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["message"], Messages.VALIDATION_ERROR)

    def test_post_does_not_create_card_for_other_users_deck(self):
        self.register_user(username="other")
        self.login_user(username="other")
        create_deck_res = self.client.post(
            reverse(UrlName.DECK_LIST),
            {
                "name": "Test deck",
            },
        )
        self.login()
        res = self.client.post(
            reverse(UrlName.CARD_LIST),
            {
                "kind": CardKind.BASIC,
                "front": "1",
                "back": "2",
                "deck": create_deck_res.data["data"]["id"],
            },
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.data["message"], Messages.DECK_NOT_FOUND)

    def test_post_uses_default_kind_if_not_provided(self):
        self.login()
        create_deck_res = self.client.post(
            reverse(UrlName.DECK_LIST),
            {
                "name": "Test deck",
            },
        )
        self.client.post(
            reverse(UrlName.CARD_LIST),
            {
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
        self.assertEqual(get_res.data["data"][0]["kind"], CardKind.BASIC)

    def test_post_requires_front_field(self):
        self.login()
        res = self.client.post(
            reverse(UrlName.CARD_LIST),
            {
                "back": "2",
                "deck": "869afa86-3f70-402e-9963-34a12a729ccd",
            },
        )
        self.assertEqual(res.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(res.data["data"]["front"], Messages.REQUIRED)

    def test_post_requires_back_field(self):
        self.login()
        res = self.client.post(
            reverse(UrlName.CARD_LIST),
            {
                "front": "1",
                "deck": "869afa86-3f70-402e-9963-34a12a729ccd",
            },
        )
        self.assertEqual(res.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(res.data["data"]["back"], Messages.REQUIRED)

    def test_post_requires_deck_field(self):
        self.login()
        res = self.client.post(
            reverse(UrlName.CARD_LIST),
            {
                "front": "1",
                "back": "2",
            },
        )
        self.assertEqual(res.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(res.data["data"]["deck"], Messages.REQUIRED)

