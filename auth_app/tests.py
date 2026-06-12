from django.urls import reverse
from rest_framework.test import APITestCase


class LogoutViewTests(APITestCase):
    """Verify that logout reliably removes authentication cookies."""

    def test_logout_deletes_auth_cookies_without_access_token(self):
        """Logout must delete cookies even when both JWTs are invalid."""
        self.client.cookies["access_token"] = "expired-access-token"
        self.client.cookies["refresh_token"] = "invalid-refresh-token"

        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, 200)
        self.assert_cookie_is_deleted(response, "access_token")
        self.assert_cookie_is_deleted(response, "refresh_token")

    def assert_cookie_is_deleted(self, response, cookie_name):
        """Assert that a response expires the selected cookie for all paths."""

        cookie = response.cookies[cookie_name]
        self.assertEqual(cookie.value, "")
        self.assertEqual(cookie["max-age"], 0)
        self.assertEqual(cookie["path"], "/")
