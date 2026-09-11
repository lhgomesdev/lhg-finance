from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class SignUpViewTests(TestCase):
    def test_signup_creates_user_and_redirects_to_login(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "password1": "senha-super-forte-123",
            "password2": "senha-super-forte-123",
        })

        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_signup_fails_with_mismatched_passwords(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "password1": "senha-super-forte-123",
            "password2": "outra-senha-diferente",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())


class LoginLockoutTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="alice", password="senha-forte-123")

    def _failed_login(self):
        return self.client.post(reverse("login"), {"username": "alice", "password": "senha-errada"})

    def test_shows_error_after_wrong_password(self):
        response = self._failed_login()

        self.assertContains(response, "senha corretos", status_code=200)

    def test_locks_out_after_too_many_failed_attempts(self):
        for _ in range(settings.AXES_FAILURE_LIMIT):
            self._failed_login()

        response = self._failed_login()

        self.assertEqual(response.status_code, 429)

    def test_correct_password_still_works_before_lockout(self):
        self._failed_login()

        response = self.client.post(reverse("login"), {"username": "alice", "password": "senha-forte-123"})

        self.assertRedirects(response, reverse("dashboard"))
