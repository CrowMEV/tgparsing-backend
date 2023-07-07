import pytest

from server import app
from settings import config


class TestTgaccount:
    tgaccounts_get: str = app.url_path_for(config.TGACCOUNT_GET_ALL)

    async def test_get_tgaccounts_by_admin(
        self,
        async_client,
        admin_login,
    ):
        response = await async_client.get(self.tgaccounts_get)
        row = response.json()

        assert response.status_code == 200
        # count of created objects
        assert len(row) == 1
        # first object ID
        assert row[0]["id"] == 1

    admin_get_data = [
        # wrong data
        ("lalala", 422),
        # correct data
        (1, 200),
    ]

    @pytest.mark.parametrize("id_row,code", admin_get_data)
    async def test_tgaccount_get_by_admin(
        self, async_client, get_session, admin_login, id_row, code
    ):
        url = app.url_path_for(config.TGACCOUNT_GET, id_row=id_row)
        response = await async_client.get(url)

        assert response.status_code == code

    admin_patch_data = [
        # wrong data
        (1, {}, 400),
        ("lalala", {"api_hash": "FREEdsdsdsds1111"}, 422),
        # correct data
        (1, {"api_hash": "FREEdsdsdsds1111"}, 200),
        (1, {"work_status": "work"}, 200),
    ]

    @pytest.mark.parametrize("id_row,data,code", admin_patch_data)
    async def test_tgaccount_patch_by_admin(
        self, async_client, get_session, admin_login, id_row, data, code
    ):
        url = app.url_path_for(config.TGACCOUNT_PATCH, id_row=id_row)
        response = await async_client.patch(url, params=data)

        assert response.status_code == code

    admin_delete_data = [
        # wrong data
        (33, 400),
        ("lalala", 422),
        # correct data
        (1, 200),
    ]

    @pytest.mark.parametrize("id_row,code", admin_get_data)
    async def test_tgaccount_delete_by_admin(
        self, async_client, get_session, admin_login, id_row, code
    ):
        url = app.url_path_for(config.TGACCOUNT_DELETE, id_row=id_row)
        response = await async_client.delete(url)

        assert response.status_code == code

    async def test_get_tgaccounts_by_user(self, async_client, user_login):
        response = await async_client.get(self.tgaccounts_get)

        assert response.status_code == 403

    async def test_tgaccount_get_by_user(
        self, async_client, get_session, user_login
    ):
        url = app.url_path_for(config.TGACCOUNT_GET, id_row=1)
        response = await async_client.get(url)

        assert response.status_code == 403

    async def test_tgaccount_patch_by_user(
        self, async_client, get_session, user_login
    ):
        url = app.url_path_for(config.TGACCOUNT_PATCH, id_row=1)
        response = await async_client.patch(url)

        assert response.status_code == 403

    async def test_tgaccount_delete_by_user(
        self,
        async_client,
        get_session,
        user_login,
    ):
        url = app.url_path_for(config.TGACCOUNT_DELETE, id_row=1)
        response = await async_client.delete(url)

        assert response.status_code == 403
