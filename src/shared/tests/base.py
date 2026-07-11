from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from shared.url_names import UrlName

User = get_user_model()


class BaseAPITestCase(APITestCase):
    def login(self):
        password = "12345678"

        user = User.objects.create_user(
            username="test",
            email="test@test.com",
            name="Test User",
            password=password,
        )

        response = self.client.post(
            reverse(UrlName.AUTH_LOGIN),
            {
                "username": user.email,
                "password": password,
            },
        )

        token = response.data["data"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return user

    def register_user(self, username):
        user = User.objects.create_user(
            username=username,
            email=f"{username}@test.com",
            name=f"Test ${username}",
            password="12345678",
        )
        return user

    def login_user(self, username):
        response = self.client.post(
            reverse(UrlName.AUTH_LOGIN),
            {
                "username": username,
                "password": "12345678",
            },
        )

        token = response.data["data"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
