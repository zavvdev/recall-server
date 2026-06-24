from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shared.messages import Messages

User = get_user_model()


class AuthRegisterTests(APITestCase):
    def test_register_should_register(self):
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

    def test_register_should_reject_if_already_created(self):
        payload = {
            "username": "john",
            "email": "john@example.com",
            "password": "strongpass123",
            "name": "John",
        }
        self.client.post(reverse("auth_register"), payload)
        response = self.client.post(reverse("auth_register"), payload)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.data["message"], Messages.AUTH_USER_CREATION_FAILED
        )
        self.assertEqual(response.data["data"], None)
        self.assertEqual(User.objects.count(), 1)

    def test_register_should_reject_invalid_username(self):
        payload = {
            "username": "1john",
            "email": "john@example.com",
            "password": "strongpass123",
            "name": "John",
        }
        response = self.client.post(reverse("auth_register"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(response.data["data"]["username"], Messages.INVALID)
        self.assertEqual(User.objects.count(), 0)

    def test_register_should_reject_invalid_password(self):
        payload = {
            "username": "john",
            "email": "john@example.com",
            "password": "123",
            "name": "John",
        }
        response = self.client.post(reverse("auth_register"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(response.data["data"]["password"], Messages.INVALID)
        self.assertEqual(User.objects.count(), 0)

    def test_register_should_require_username(self):
        payload = {
            "email": "john@example.com",
            "password": "12345678",
            "name": "John",
        }
        response = self.client.post(reverse("auth_register"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(response.data["data"]["username"], Messages.REQUIRED)
        self.assertEqual(User.objects.count(), 0)

    def test_register_should_require_email(self):
        payload = {
            "username": "john",
            "password": "12345678",
            "name": "John",
        }
        response = self.client.post(reverse("auth_register"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(response.data["data"]["email"], Messages.REQUIRED)
        self.assertEqual(User.objects.count(), 0)

    def test_register_should_require_password(self):
        payload = {
            "username": "john",
            "email": "john@example.com",
            "name": "John",
        }
        response = self.client.post(reverse("auth_register"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(response.data["data"]["password"], Messages.REQUIRED)
        self.assertEqual(User.objects.count(), 0)

    def test_register_should_require_name(self):
        payload = {
            "username": "john",
            "email": "john@example.com",
            "password": "12345678",
        }
        response = self.client.post(reverse("auth_register"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], Messages.VALIDATION_ERROR)
        self.assertEqual(response.data["data"]["name"], Messages.REQUIRED)
        self.assertEqual(User.objects.count(), 0)
