import pytest
from server import app
from settings import config


class TestTgmember:
    tgmembers_get: str = app.url_path_for(config.MEMBER_GET_ALL)
    get_tgmembers_params = [
        ({"chats.id": 1}, 200),
    ]
    get_delete_tgmember_data = [
        # wrong data
        ("lalala", 422),
        # correct data
        (1, 200),
    ]

    @pytest.mark.parametrize("params,code", get_tgmembers_params)
    async def test_get_tgmembers_by_user(
        self, async_client, user_login, params, code
    ):
        response = await async_client.get(self.tgmembers_get, params=params)
        row = response.json()

        assert response.status_code == code
        # count of created objects with filter in params
        assert len(row) == 1
        # first object ID with filter in params
        assert row[0]["id"] == 1

    @pytest.mark.parametrize("id_row,code", get_delete_tgmember_data)
    async def test_delete_tgmember_by_user(
        self, async_client, user_login, id_row, code
    ):
        url = app.url_path_for(config.MEMBER_DELETE, id_row=id_row)
        response = await async_client.get(url)

        assert response.status_code == code


class TestChat:
    chats_get: str = app.url_path_for(config.CHAT_GET_ALL)
    get_delete_chat_data = [
        # wrong data
        ("lalala", 422),
        # correct data
        (1, 200),
    ]

    async def test_get_chats_by_user(self, async_client, user_login):
        response = await async_client.get(self.chats_get)
        row = response.json()

        assert response.status_code == 200
        # count of created objects
        assert len(row) == 1
        # first object ID
        assert row[0]["id"] == 1

    @pytest.mark.parametrize("id_row,code", get_delete_chat_data)
    async def test_get_chat_by_user(
        self, async_client, user_login, id_row, code
    ):
        url = app.url_path_for(config.CHAT_BY_ID, id_row=id_row)
        response = await async_client.get(url)

        assert response.status_code == code

    @pytest.mark.parametrize("id_row,code", get_delete_chat_data)
    async def test_delete_chat_by_user(
        self, async_client, user_login, id_row, code
    ):
        url = app.url_path_for(config.MEMBER_DELETE, id_row=id_row)
        response = await async_client.get(url)

        assert response.status_code == code
