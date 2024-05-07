from http import HTTPStatus

from api.base import BaseTest


class TestTodo(BaseTest):
    def setUp(self):
        # Create test users
        self.user = self._create_account(
            username="foo@buzz.com",
        )
        self.token = self._get_api_token(user=self.user)

    def test_todo(self):
        # Create Todo
        name = "#1 todo"
        response = self._post(
            "/api/todos/",
            token=self.token,
            data={"name": name},
        )

        res_data = response.data
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data["name"], name)

        # Get List Todo
        response = self._get(
            "/api/todos/",
            token=self.token,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), 1)

        # Detail Todo
        response = self._get(
            f"/api/todos/{res_data.get('id')}/",
            token=self.token,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data.get("id"), res_data.get("id"))

        response = self._get(
            f"/api/todos/{res_data.get('id')}/",
            token=self.token,
        )

        # Update Todo
        response = self._put(
            f"/api/todos/{res_data.get('id')}/",
            token=self.token,
            data={"done": True},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.data.get("done"))

        # Delete Todo
        response = self._delete(
            f"/api/todos/{res_data.get('id')}/",
            token=self.token,
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
