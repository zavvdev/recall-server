from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


# TODO: Add more tests
class AuthRefreshTests(APITestCase):
    def test_refresh_token(self):
        User.objects.create_user(
            username="john", email="john@example.com", password="strongpass123", name="John"
        )
        login_resp = self.client.post(
            reverse("auth_login"), {"username": "john", "password": "strongpass123"}
        )
        refresh_token = login_resp.data["data"]["refresh"]
        response = self.client.post(reverse("auth_refresh"), {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data["data"])
