import decimal

import pytest
from server import app
from settings import config


class TestTariff:
    tariffs_get: str = app.url_path_for(config.TARIFF_GET_ALL)
    tariff_toggle_status: str = app.url_path_for(config.TARIFF_TOGGLE_STATUS)
    tariff_add: str = app.url_path_for(config.TARIFF_ADD)

    async def test_get_tariffs_by_user(
        self,
        async_client,
        user_login,
    ):
        response = await async_client.get(self.tariffs_get)
        row = response.json()

        assert response.status_code == 200
        # count of created objects
        assert len(row) == 1
        # first object ID
        assert row[0]["id"] == 1

    async def test_tariff_purachase_by_user(self, async_client, user_login):
        url = app.url_path_for(config.TARIFF_PURCHASE, id_row=1)
        response = await async_client.post(url)
        row = response.json()

        assert response.status_code == 200
        # changing user balance after purchaice
        assert decimal.Decimal(row["balance"]) == (1200 - 1200)
        # confirmation of subscription with the correct tariff
        assert row["subscribe"]["tariff_id"] == 1
        assert row["subscribe"]["auto_debit"] is True

    user_get_data = [
        # wrong data
        ("lalala", 422),
        # correct data
        (1, 200),
    ]

    @pytest.mark.parametrize("id_row,code", user_get_data)
    async def test_get_tariff_by_user(
        self, async_client, get_session, user_login, id_row, code
    ):
        url = app.url_path_for(config.TARIFF_GET, id_row=id_row)
        response = await async_client.get(url)

        assert response.status_code == code

    async def test_toggle_tariff_auto_write_off_by_user(
        self, async_client, user_login
    ):
        response = await async_client.post(self.tariff_toggle_status)
        row = response.json()

        assert response.status_code == 200
        # confirmation of changing
        assert row["auto_debit"] is False

    async def test_patch_tariff_by_user(
        self, async_client, get_session, user_login
    ):
        url = app.url_path_for(config.TARIFF_PATCH, id_row=1)
        response = await async_client.patch(url)

        assert response.status_code == 403

    async def test_delete_tariff_by_user(
        self, async_client, get_session, user_login
    ):
        url = app.url_path_for(config.TARIFF_DELETE, id_row=1)
        response = await async_client.delete(url)

        assert response.status_code == 403

    superuser_create_data = [
        # not unique name data
        (
            {
                "name": "Test",
                "description": "Super tariff",
                "limitation_days": 30,
                "price": 2000,
                "options": {
                    "parsers_per_day": 18,
                    "simultaneous_parsing": 15,
                    "geo": True,
                    "members": True,
                    "activity": True,
                },
                "active": True,
                "archive": True,
            },
            400,
        ),
        # correct data
        (
            {
                "name": "Super",
                "description": "Super tariff",
                "limitation_days": 30,
                "price": 2000,
                "options": {
                    "parsers_per_day": 18,
                    "simultaneous_parsing": 15,
                    "geo": True,
                    "members": True,
                    "activity": True,
                },
                "active": True,
                "archive": True,
            },
            200,
        ),
    ]

    @pytest.mark.parametrize("data,code", superuser_create_data)
    async def test_create_tariff_by_superuser(
        self, async_client, superuser_login, data, code
    ):
        response = await async_client.post(self.tariff_add, json=data)

        assert response.status_code == code

    async def test_get_tariffs_by_superuser(
        self,
        async_client,
        superuser_login,
    ):
        response = await async_client.get(self.tariffs_get)
        row = response.json()

        assert response.status_code == 200
        # count of created objects
        assert len(row) == 2

    async def test_get_tariff_by_superuser(
        self,
        async_client,
        get_session,
        superuser_login,
    ):
        url = app.url_path_for(config.TARIFF_GET, id_row=2)
        response = await async_client.get(url)

        assert response.status_code == 200

    superuser_patch_data = [
        # wrong data
        (
            2,
            {
                "active": 22,
            },
            422,
        ),
        # correct data
        (
            2,
            {
                "name": "Tratata",
                "description": "Tarar tariff",
                "limitation_days": 20,
                "price": 5000,
                "options": {
                    "parsers_per_day": 38,
                    "simultaneous_parsing": 45,
                    "geo": True,
                    "members": True,
                    "activity": True,
                },
                "active": True,
                "archive": True,
            },
            200,
        ),
    ]

    @pytest.mark.parametrize("id_row,data,code", superuser_patch_data)
    async def test_patch_tariff_by_superuser(
        self, async_client, get_session, superuser_login, id_row, data, code
    ):
        url = app.url_path_for(config.TARIFF_PATCH, id_row=id_row)
        response = await async_client.patch(url, json=data)

        assert response.status_code == code

    async def test_delete_tariff_by_superuser(
        self, async_client, get_session, superuser_login
    ):
        url = app.url_path_for(config.TARIFF_DELETE, id_row=2)
        response = await async_client.delete(url)

        assert response.status_code == 200
