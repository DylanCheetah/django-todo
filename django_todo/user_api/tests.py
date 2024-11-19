from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Test Cases
# ==========
class UserAPITests(APITestCase):
    def test_user_registration(self):
        # Create a test user
        url = reverse("user-register")
        data = {
            "username": "DylanCheetah",
            "password": "cat",
            "email": "dylan.the.cheetah@gmail.com"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username="DylanCheetah")
        self.assertEqual(user.email, data["email"])

    def test_user_login(self):
        # Create test user
        User.objects.create_user(
            username="DylanCheetah",
            password="cat",
            email="dylan.the.cheetah@gmail.com"
        )

        # Attempt to log in
        url = reverse("token_obtain_pair")
        data = {
            "username": "DylanCheetah",
            "password": "cat"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.json()
        self.assertTrue("access" in self.token and "refresh" in self.token)

    def test_user_change_password(self):
        # Create test user
        User.objects.create_user(
            username="DylanCheetah",
            password="cat",
            email="dylan.the.cheetah@gmail.com"
        )

        # Attempt to change password
        url = reverse("user-change-password")
        headers = {
            "Authorization": f"Bearer {self.token['access']}"
        }
        data = {
            "password": "cheetah"
        }
        response = self.client.put(url, headers=headers, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
