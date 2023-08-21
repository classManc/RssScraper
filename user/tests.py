from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
    
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
