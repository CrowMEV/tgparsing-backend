import pytest

from server import app
from settings import config


class TestTgaccount:
    tgaccounts_get: str = app.url_path_for(config.TGACCOUNT_GET_ALL)
    tgaccount_url: str = app.url_path_for(config.TGACCOUNT_CREATE)

    admin_tgaccount_data = [
        # wrong api_id
        ({"api_id": "api", "api_hash": "123api12hash",
          "session_string": "123session12345"}, 422),
        # without api_hash
        ({"api_id": "api", "session_string": "123session12345"}, 422),
        # without session_string
        ({"api_id": "api", "api_hash": "123api12hash"}, 422),
        # correct data
        ({"api_id": 1, "api_hash": "123api12hash",
          "session_string": "123session12345"}, 201)
    ]

    @pytest.mark.parametrize("data,code", admin_tgaccount_data)
    async def test_tgaccount_create_by_admin(
        self, async_client, admin_login, data, code
    ):
        response = await async_client.post(self.tgaccount_url, json=data)

        assert response.status_code == code

    user_tgaccount_data = [
       ({"api_id": 1, "api_hash": "123api12hash",
        "session_string": "123session12345"}, 403)
    ]

    @pytest.mark.parametrize("data,code", user_tgaccount_data)
    async def test_tgaccount_create_by_user(
        self, async_client, user_login, data, code
    ):
        response = await async_client.post(self.tgaccount_url, json=data)

        assert response.status_code == code

    async def test_get_tgaccounts_by_admin(self, async_client, admin_login):
        response = await async_client.get(self.tgaccounts_get)

        assert response.status_code == 200

    async def test_get_tgaccounts_by_user(self, async_client, user_login):
        response = await async_client.get(self.tgaccounts_get)

        assert response.status_code == 403
