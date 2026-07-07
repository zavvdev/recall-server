from django.urls import reverse
from rest_framework import status

from shared.messages import Messages
from shared.models import Visibility
from shared.tests.base import BaseAPITestCase
from shared.url_names import UrlName


class DeckDetailViewTest(BaseAPITestCase):
    def test_get_retrieves_deck_by_id(self):
        self.login()
        create_res = self.client.post(
            reverse(UrlName.DECK_LIST),
            {
                "name": "Test deck",
            },
        )
        get_res = self.client.get(
            reverse(
                UrlName.DECK_DETAIL,
                kwargs={"pk": create_res.data["data"]["id"]},
            ),
        )
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertEqual(get_res.data["message"], Messages.OK)
        self.assertEqual(
            get_res.data["data"]["id"], create_res.data["data"]["id"]
        )
        self.assertEqual(
            get_res.data["data"]["name"], create_res.data["data"]["name"]
        )
        self.assertEqual(
            get_res.data["data"]["visibility"],
            create_res.data["data"]["visibility"],
        )


    def test_get_returns_404_if_not_found(self):
        self.login()
        get_res = self.client.get(
            reverse(
                UrlName.DECK_DETAIL,
                kwargs={"pk": "869afa86-3f70-402e-9963-34a12a729ccd"},
            ),
        )
        self.assertEqual(get_res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get_res.data["message"], Messages.NOT_FOUND)
        self.assertEqual(get_res.data["data"], None)


    def test_patch_updates_deck_by_id(self):
        user = self.login()
        create_res = self.client.post(
            reverse(UrlName.DECK_LIST),
            {
                "name": "Test deck",
            },
        )
        created_deck_id = create_res.data["data"]["id"]
        self.client.patch(
            reverse(
                UrlName.DECK_DETAIL,
                kwargs={"pk": created_deck_id},
            ),
            {"name": "Updated", "visibility": Visibility.PUBLIC}
        )
        deck = user.decks.get(pk=created_deck_id)
        self.assertEqual(deck.name, "Updated")
        self.assertEqual(deck.visibility, Visibility.PUBLIC)


    def test_patch_returns_404_if_not_found(self):
        self.login()
        patch_res = self.client.patch(
            reverse(
                UrlName.DECK_DETAIL,
                kwargs={"pk": "869afa86-3f70-402e-9963-34a12a729ccd"},
            ),
            {"name": "Updated", "visibility": Visibility.PUBLIC}
        )
        self.assertEqual(patch_res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(patch_res.data["message"], Messages.NOT_FOUND)
        self.assertEqual(patch_res.data["data"], None)


    def test_delete_deletes_deck_by_id(self):
        user = self.login()
        create_res = self.client.post(
            reverse(UrlName.DECK_LIST),
            {
                "name": "Test deck",
            },
        )
        created_deck_id = create_res.data["data"]["id"]
        self.assertEqual(len(user.decks.all()), 1)
        delete_res = self.client.delete(
            reverse(
                UrlName.DECK_DETAIL,
                kwargs={"pk": created_deck_id},
            ),
        )
        self.assertEqual(delete_res.data["message"], Messages.OK)
        self.assertEqual(len(user.decks.all()), 0)


    def test_delete_returns_404_if_not_found(self):
        self.login()
        patch_res = self.client.delete(
            reverse(
                UrlName.DECK_DETAIL,
                kwargs={"pk": "869afa86-3f70-402e-9963-34a12a729ccd"},
            ),
        )
        self.assertEqual(patch_res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(patch_res.data["message"], Messages.NOT_FOUND)
        self.assertEqual(patch_res.data["data"], None)
