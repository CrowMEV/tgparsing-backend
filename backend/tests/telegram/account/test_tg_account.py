import pytest
import random
import sqlalchemy as sa

from server import app
from settings import config
from services.telegram.account.models import TgAccount


class TestTgaccount:
    tgaccounts_get: str = app.url_path_for(config.TGACCOUNT_GET_ALL)

    async def test_get_tgaccounts_by_admin(
        self, async_client, admin_login
    ):
        response = await async_client.get(self.tgaccounts_get)

        assert response.status_code == 200

    async def get_tgaccount_id(self, session):
        api_id = random.randint(2, 100000)
        data = {"api_id": api_id, "api_hash": "123api12hash",
                "session_string": "123session12345",
                "phone_number": "+79997776644"}

        account = TgAccount(**data)
        session.add(account)
        await session.commit()

        stmt = sa.select(TgAccount).where(TgAccount.api_id == data["api_id"])
        result = await session.execute(stmt)
        account_get = result.scalars().first()

        return account_get.id

    async def test_tgaccount_get_by_admin(
        self, async_client, get_session, admin_login
    ):
        id_row = await self.get_tgaccount_id(get_session)

        tgaccount_get: str = app.url_path_for(
            config.TGACCOUNT_GET, id_row=id_row
        )

        response = await async_client.get(tgaccount_get)

        assert response.status_code == 200

    async def test_tgaccount_delete_by_admin(
        self, async_client, get_session, admin_login,
    ):
        id_row = await self.get_tgaccount_id(get_session)

        tgaccount_delete: str = app.url_path_for(
            config.TGACCOUNT_DELETE, id_row=id_row
        )

        response = await async_client.delete(tgaccount_delete)

        assert response.status_code == 200

    admin_patch_data = [
        # wrong data
        ({}, 400),
        # correct data
        ({"api_hash": "FREEdsdsdsds1111"}, 200),
        ({"work_status": "work"}, 200),
    ]

    @pytest.mark.parametrize("data,code", admin_patch_data)
    async def test_tgaccount_patch_by_admin(
        self, async_client, get_session, admin_login, data, code
    ):
        id_row = await self.get_tgaccount_id(get_session)

        tgaccount_patch: str = app.url_path_for(
            config.TGACCOUNT_PATCH, id_row=id_row
        )

        response = await async_client.patch(tgaccount_patch, params=data)

        assert response.status_code == code

    async def test_get_tgaccounts_by_user(
        self, async_client, user_login
    ):
        response = await async_client.get(self.tgaccounts_get)

        assert response.status_code == 403

    async def test_tgaccount_get_by_user(
        self, async_client, get_session, user_login
    ):
        id_row = await self.get_tgaccount_id(get_session)

        tgaccount_get: str = app.url_path_for(
            config.TGACCOUNT_GET, id_row=id_row
        )

        response = await async_client.get(tgaccount_get)

        assert response.status_code == 403

    async def test_tgaccount_delete_by_user(
        self, async_client, get_session, user_login,
    ):
        id_row = await self.get_tgaccount_id(get_session)

        tgaccount_delete: str = app.url_path_for(
            config.TGACCOUNT_DELETE, id_row=id_row
        )

        response = await async_client.delete(tgaccount_delete)

        assert response.status_code == 403

    user_patch_data = [
        ({"work_status": "work"}, 403),
    ]

    @pytest.mark.parametrize("data,code", user_patch_data)
    async def test_tgaccount_patch_by_user(
        self, async_client, get_session, user_login, data, code
    ):
        id_row = await self.get_tgaccount_id(get_session)

        tgaccount_patch: str = app.url_path_for(
            config.TGACCOUNT_PATCH, id_row=id_row
        )

        response = await async_client.patch(tgaccount_patch, params=data)

        assert response.status_code == code
