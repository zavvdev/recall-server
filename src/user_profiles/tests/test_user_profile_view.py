from django.urls import reverse
from rest_framework import status

from shared.messages import Messages
from shared.tests.base import BaseAPITestCase
from user_profiles.models import ProfileLang, ProfileTheme, ProfileVisibility


class UserProfileViewTest(BaseAPITestCase):
    def test_retrieves_user_profile(self):
        self.login()
        response = self.client.get(reverse("user_profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], Messages.OK)
        self.assertEqual(
            response.data["data"]["visibility"], ProfileVisibility.PRIVATE
        )
        self.assertEqual(response.data["data"]["language"], ProfileLang.EN)
        self.assertEqual(response.data["data"]["theme"], ProfileTheme.LIGHT)

    def test_updates_user_profile(self):
        self.login()
        response = self.client.get(reverse("user_profile"))
        
        self.assertEqual(
            response.data["data"]["visibility"], ProfileVisibility.PRIVATE
        )
        self.assertEqual(response.data["data"]["language"], ProfileLang.EN)
        self.assertEqual(response.data["data"]["theme"], ProfileTheme.LIGHT)
        
        self.client.put(reverse("user_profile"), {
            "visibility": ProfileVisibility.PUBLIC,
            "language": ProfileLang.EN,
            "theme": ProfileTheme.DARK,
        })

        updated = self.client.get(reverse("user_profile"))

        self.assertEqual(
            updated.data["data"]["visibility"], ProfileVisibility.PUBLIC
        )
        self.assertEqual(updated.data["data"]["language"], ProfileLang.EN)
        self.assertEqual(updated.data["data"]["theme"], ProfileTheme.DARK)
