from django.urls import reverse
from rest_framework import status

from shared.messages import Messages
from shared.models import Visibility
from shared.tests.base import BaseAPITestCase
from shared.url_names import UrlName


class UserProfileViewTest(BaseAPITestCase):
    def test_get_retrieves_decks_for_user(self):
        self.login()

        self.client.post(
            reverse(UrlName.DECK_LIST),
            {
                "name": "Test deck",
            },
        )

        response = self.client.get(
            reverse(UrlName.DECK_LIST),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], Messages.OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["name"], "Test deck")

    def test_post_creates_deck_with_default_visibility(self):
        user = self.login()

        self.assertEqual(len(user.decks.all()), 0)

        self.client.post(
            reverse(UrlName.DECK_LIST),
            {
                "name": "Test deck",
            },
        )

        self.assertEqual(len(user.decks.all()), 1)
        deck = user.decks.all()[0]
        self.assertEqual(deck.visibility, Visibility.PRIVATE)

    def test_post_creates_deck_with_custom_visibility(self):
        user = self.login()

        self.client.post(
            reverse(UrlName.DECK_LIST),
            {
                "name": "Test deck",
                "visibility": Visibility.PUBLIC,
            },
        )

        deck = user.decks.all()[0]
        self.assertEqual(deck.visibility, Visibility.PUBLIC)

    def test_post_requires_name(self):
        self.login()

        response = self.client.post(
            reverse(UrlName.DECK_LIST),
            {
                "visibility": Visibility.PUBLIC,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(response.data["data"]["name"], Messages.REQUIRED)
