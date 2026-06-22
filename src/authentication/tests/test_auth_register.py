from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shared.messages import Messages

User = get_user_model()


# TODO: Add more tests
class AuthRegisterTests(APITestCase):
    def test_register_user(self):
        payload = {
            "username": "john",
            "email": "john@example.com",
            "password": "strongpass123",
            "name": "John",
        }
        response = self.client.post(reverse("auth_register"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], Messages.OK)
        self.assertEqual(response.data["data"], None)
        self.assertEqual(User.objects.count(), 1)
