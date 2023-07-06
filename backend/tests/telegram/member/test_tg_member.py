import pytest

from server import app
from settings import config


class TestTgmember:
    tgmembers_get: str = app.url_path_for(config.MEMBER_GET_ALL)

    async def test_get_tgmembers_by_user(
        self,
        async_client,
        user_login
    ):
        response = await async_client.get(self.tgmembers_get)
        row = response.json()

        assert response.status_code == 200
        # count of created objects
        assert len(row) == 1
        # first object ID
        assert row[0]["user_id"] == 123

    user_get_data = [
        # wrong data
        ("lalala", 422),
        # correct data
        (1, 200),
    ]

    @pytest.mark.parametrize("id_row,code", user_get_data)
    async def test_get_tgmember_by_user(
        self,
        async_client,
        user_login, id_row, code
    ):
        url: str = app.url_path_for(config.MEMBER_BY_ID, id_row=id_row)
        response = await async_client.get(url)

        assert response.status_code == code


class TestChat:
    chats_get: str = app.url_path_for(config.CHAT_GET_ALL)

    async def test_get_chats_by_user(
        self,
        async_client,
        user_login
    ):
        response = await async_client.get(self.chats_get)
        row = response.json()

        assert response.status_code == 200
        # count of created objects
        assert len(row) == 1
        # first object ID
        assert row[0]["username"] == "oldstars"

    user_get_data = [
        # wrong data
        ("lalala", 422),
        # correct data
        (1, 200),
    ]

    @pytest.mark.parametrize("id_row,code", user_get_data)
    async def test_get_chat_by_user(
        self,
        async_client,
        user_login, id_row, code
    ):
        url: str = app.url_path_for(config.CHAT_BY_ID, id_row=id_row)
        response = await async_client.get(url)

        assert response.status_code == code
