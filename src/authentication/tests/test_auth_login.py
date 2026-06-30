from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shared.messages import Messages
from shared.url_names import UrlName

User = get_user_model()


class AuthLoginTests(APITestCase):
    def test_login_should_login_with_username(self):
        User.objects.create_user(
            username="john",
            email="john@example.com",
            password="strongpass123",
            name="John",
        )
        payload = {"username": "john", "password": "strongpass123"}
        response = self.client.post(reverse(UrlName.AUTH_LOGIN), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], Messages.OK)
        self.assertIn("access", response.data["data"])
        self.assertIn("refresh", response.data["data"])

    def test_login_should_login_with_email(self):
        User.objects.create_user(
            username="john",
            email="john@example.com",
            password="strongpass123",
            name="John",
        )
        payload = {"username": "john@example.com", "password": "strongpass123"}
        response = self.client.post(reverse(UrlName.AUTH_LOGIN), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], Messages.OK)
        self.assertIn("access", response.data["data"])
        self.assertIn("refresh", response.data["data"])

    def test_login_should_reject_if_not_found(self):
        response = self.client.post(
            reverse(UrlName.AUTH_LOGIN),
            {"username": "nofound", "password": "strongpass123"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"], Messages.AUTH_INVALID_CREDENTIALS
        )
        self.assertEqual(response.data["data"], None)

    def test_login_should_reject_invalid_password(self):
        response = self.client.post(
            reverse(UrlName.AUTH_LOGIN), {"username": "john", "password": "123"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(response.data["data"]["password"], Messages.INVALID)

    def test_login_should_reject_invalid_username(self):
        response = self.client.post(
            reverse(UrlName.AUTH_LOGIN),
            {"username": "1asd", "password": "12345678"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(response.data["data"]["username"], Messages.INVALID)

    def test_login_should_require_password(self):
        response = self.client.post(
            reverse(UrlName.AUTH_LOGIN), {"username": "john"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(response.data["data"]["password"], Messages.REQUIRED)

    def test_login_should_require_username(self):
        response = self.client.post(
            reverse(UrlName.AUTH_LOGIN), {"password": "12345678"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(response.data["data"]["username"], Messages.REQUIRED)
