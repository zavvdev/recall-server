from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shared.messages import Messages

User = get_user_model()


class AuthRefreshTests(APITestCase):
    def test_refresh_token_should_refresh(self):
        User.objects.create_user(
            username="john",
            email="john@example.com",
            password="strongpass123",
            name="John",
        )
        login_resp = self.client.post(
            reverse("auth_login"),
            {"username": "john", "password": "strongpass123"},
        )
        refresh_token = login_resp.data["data"]["refresh"]
        response = self.client.post(
            reverse("auth_refresh"), {"refresh": refresh_token}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data["data"])

    def test_refresh_token_should_reject_if_invalid(self):
        response = self.client.post(reverse("auth_refresh"), {"refresh": "123"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], Messages.NOT_AUTHENTICATED)
        self.assertEqual(response.data["data"], None)

    def test_refresh_should_require_refresh_field(self):
        response = self.client.post(reverse("auth_refresh"), {"refr": "123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(response.data["data"]["refresh"], Messages.REQUIRED)
