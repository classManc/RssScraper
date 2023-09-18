from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import ResetToken
from rest_framework import status
import uuid
from django.contrib.auth.models import User


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="josephajakaye924@gmail.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)
        self.reset_token = uuid.uuid4().hex
        self.user_token = ResetToken.objects.create(token=self.reset_token, user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
    
    def test_register_user(self):
        url = reverse("list_user")
        data = {
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "testpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().username, "testuser2")

    def test_login_user(self):
        url = reverse("user_login")
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
    
    def test_forgot_password(self):
        url = reverse("forgot_password")
        data = {'email': self.user.email}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
    
    def test_invalid_forgot_password(self):
        url = reverse("forgot_password")
        data = {'email': 'testing1@gmail.com'}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # self.assertIn("message", response.data)
    
    def test_reset_password(self):
        url = reverse("reset_password")
        data = {'token': self.user_token.token, 'password': 'testing1#'}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
    
    def invalid_test_reset_password(self):
        url = reverse("reset_password")
        data = {'token': '', 'password': 'testing1#'}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # self.assertIn("message", response.data)
    
    def test_reset_auth_password(self):
        url = reverse("reset_auth_user_password")
        data = {'old_password': "testpassword", 'new_password': 'testing1#'}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def invalid_test_reset_auth_password(self):
        url = reverse("reset_auth_user_password")
        data = {'old_password':'password', 'new_password': 'testing1#'}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

