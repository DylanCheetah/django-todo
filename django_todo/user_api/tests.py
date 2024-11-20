from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
import jwt
from rest_framework import status
from rest_framework.test import APITestCase


# Test Cases
# ==========
class UserAPITests(APITestCase):
    def test_user_registration_valid(self):
        # Create a test user
        url = reverse("user-register")
        data = {
            "username": "DylanCheetah",
            "password": "cheetahs_are_awesome",
            "email": "dylan.the.cheetah@gmail.com"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username="DylanCheetah")
        self.assertEqual(user.email, data["email"])
        self.assertFalse(user.is_active)

    def test_user_registration_invalid(self):
        # Create a test user
        url = reverse("user-register")
        data = {
            "username": "",
            "password": "",
            "email": "dylan.the.cheetah@gmail.com"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate(self):
        # Create a test user
        url = reverse("user-register")
        data = {
            "username": "DylanCheetah",
            "password": "cheetahs_are_awesome",
            "email": "dylan.the.cheetah@gmail.com"
        }
        response = self.client.post(url, data, format="json")

        # Attempt to create duplicate user
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_verify_email(self):
        # Create test user
        user = User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com",
            is_active=False
        )

        # Generate fake verification token for testing
        token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY)

        # Attempt to verify email address
        url = reverse("user-verify") + f"?token={token}"
        response = self.client.get(url)
        self.assertContains(
            response,
            "Email Verified",
            status_code=status.HTTP_200_OK
        )

    def test_user_verify_email_failure(self):
        # Create test user
        User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com",
            is_active=False
        )

        # Create fake verification token for testing
        token = "cat"

        # Attempt to verify email address
        url = reverse("user-verify") + f"?token={token}"
        response = self.client.get(url)
        self.assertContains(
            response,
            "Email Verification Failed",
            status_code=status.HTTP_200_OK
        )

    def test_user_login_valid(self):
        # Create test user
        User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Attempt to log in with valid credentials
        url = reverse("token_obtain_pair")
        data = {
            "username": "DylanCheetah",
            "password": "cheetahs_are_awesome"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.json()
        self.assertTrue("access" in token and "refresh" in token)

    def test_user_login_invalid(self):
        # Create test user
        User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Attempt to log in with invalid credentials
        url = reverse("token_obtain_pair")
        data = {
            "username": "DylanCheetah",
            "password": "cheetahs_are_fabulous"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_change_password_valid(self):
        # Create test user
        user = User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Force authentication
        self.client.force_authenticate(user)

        # Attempt to set valid password
        url = reverse("user-change-password")
        data = {
            "password": "cheetahs_are_great"
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_change_password_invalid(self):
        # Create test user
        user = User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Force authentication
        self.client.force_authenticate(user)

        # Attempt to set invalid password
        url = reverse("user-change-password")
        data = {
            "password": "cat"
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_change_password_unauthorized(self):
        # Create test user
        User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Attempt to set valid password without logging in
        url = reverse("user-change-password")
        data = {
            "password": "cheetahs_are_fabulous"
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
