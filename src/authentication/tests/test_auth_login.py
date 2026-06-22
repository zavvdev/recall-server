from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shared.messages import Messages

User = get_user_model()


# TODO: Add more tests
class AuthLoginTests(APITestCase):
    def test_login(self):
        User.objects.create_user(
            username="john", email="john@example.com", password="strongpass123", name="John"
        )
        payload = {"username": "john", "password": "strongpass123"}
        response = self.client.post(reverse("auth_login"), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], Messages.OK)
        self.assertIn("access", response.data["data"])
        self.assertIn("refresh", response.data["data"])
