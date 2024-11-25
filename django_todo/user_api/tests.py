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

    def test_user_set_password_valid(self):
        # Create test user
        user = User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Force authentication
        self.client.force_authenticate(user)

        # Attempt to set valid password
        url = reverse("user-set-password")
        data = {
            "password": "cheetahs_are_great"
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_set_password_invalid(self):
        # Create test user
        user = User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Force authentication
        self.client.force_authenticate(user)

        # Attempt to set invalid password
        url = reverse("user-set-password")
        data = {
            "password": "cat"
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_set_password_unauthorized(self):
        # Create test user
        User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Attempt to set valid password without logging in
        url = reverse("user-set-password")
        data = {
            "password": "cheetahs_are_fabulous"
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_set_email_valid(self):
        # Create test user
        user = User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Force authentication
        self.client.force_authenticate(user)

        # Attempt to set a valid email address
        url = reverse("user-set-email")
        data = {
            "email": "dylan_the_cheetah@outlook.com"
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(user.email, data["email"])
        self.assertFalse(user.is_active)

    def test_user_set_email_invalid(self):
        # Create test user
        user = User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Force authentication
        self.client.force_authenticate(user)

        # Attempt to set an invalid email address
        url = reverse("user-set-email")
        data = {
            "email": "junk"
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_set_email_unauthorized(self):
        # Create test user
        User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Attempt to set a valid email address
        url = reverse("user-set-email")
        data = {
            "email": "dylan_the_cheetah@outlook.com"
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_delete_valid(self):
        # Create test user
        user = User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Force authentication
        self.client.force_authenticate(user)

        # Attempt to delete the user account
        url = reverse("user-delete")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            User.objects.filter(username="DylanCheetah").count(),
            0
        )

    def test_user_delete_unauthorized(self):
        # Create test user
        User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Attempt to delete the user account
        url = reverse("user-delete")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_me_valid(self):
        # Create test user
        user = User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Force authentication
        self.client.force_authenticate(user)

        # Attempt to fetch info for the authenticated user
        url = reverse("user-me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.json()
        self.assertTrue("url" in payload and "id" in payload)
        self.assertEqual(payload["username"], "DylanCheetah")
        self.assertEqual(payload["email"], "dylan.the.cheetah@gmail.com")

    def test_user_me_unauthorized(self):
        # Create test user
        User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Attempt to fetch info for the authenticated user
        url = reverse("user-me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reset_password_request_valid(self):
        # Create test user
        User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Send valid password reset request
        url = reverse("user-reset-password")
        data = {
            "email": "dylan.the.cheetah@gmail.com"
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reset_password_request_invalid(self):
        # Create test user
        User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Send invalid password reset request
        url = reverse("user-reset-password")
        data = {
            "email": "junk"
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_finish_valid(self):
        # Create test user
        user = User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Generate fake password reset token for testing purposes
        token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY)

        # Send valid password reset request
        url = reverse("user-reset-password-finish")
        data = {
            "token": token,
            "password": "cheetahs_are_cool"
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reset_password_finish_invalid(self):
        # Create test user
        user = User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Generate fake password reset token for testing purposes
        token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY)

        # Send valid password reset request
        url = reverse("user-reset-password-finish")
        data = {
            "token": token,
            "password": "cat"
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_finish_unauthorized(self):
        # Create test user
        User.objects.create_user(
            username="DylanCheetah",
            password="cheetahs_are_awesome",
            email="dylan.the.cheetah@gmail.com"
        )

        # Generate fake password reset token for testing purposes
        token = "trash-token-that-won't-work"

        # Send valid password reset request
        url = reverse("user-reset-password-finish")
        data = {
            "token": token,
            "password": "cheetahs_are_cool"
        }
        response = self.client.put(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
