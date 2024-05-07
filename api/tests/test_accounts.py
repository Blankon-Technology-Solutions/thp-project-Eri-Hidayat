from http import HTTPStatus

from api.base import BaseTest


class TestAccount(BaseTest):
    def setUp(self):
        # Create test users
        self.user = self._create_account(
            username="foo@buzz.com",
        )
        self.token = self._get_api_token(user=self.user)

    def test_register_login(self):
        email = self._create_fake_email()
        pwd = "All-f0r-1"

        res = self._post(
            "/api/accounts/register/",
            data={"email": email, "password": pwd},
        )

        self.assertEqual(res.status_code, HTTPStatus.OK)

        res = self._post(
            "/api/accounts/login/",
            data={"email": email, "password": pwd},
        )
        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_logout(self):
        res = self._get("/api/accounts/logout/", token=self.token)
        self.assertEqual(res.status_code, HTTPStatus.NO_CONTENT)

    def test_no_token(self):
        res = self._get("/api/accounts/")
        self.assertEqual(res.status_code, HTTPStatus.BAD_REQUEST)
