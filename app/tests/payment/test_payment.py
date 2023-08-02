import json
from urllib import parse

import pytest
import sqlalchemy as sa
from server import app
from services.payment.models import Payment
from settings import config
from tests import conftest


class TestPayment:
    payments_get: str = app.url_path_for(config.PAYMENTS_GET)

    payment_data = [
        # wrong data
        (0, 422),
        (1.123, 422),
        # correct data
        (1, 200),
    ]

    @pytest.mark.parametrize("tariff_id,code", payment_data[:-1])
    async def test_add_payment_wrong_data(
        self, async_client, user_login, tariff_id, code
    ):
        payment_url: str = app.url_path_for(
            config.PAYMENT_ADD, tariff_id=tariff_id
        )
        response = await async_client.post(
            payment_url,
        )
        assert response.status_code == code

    @pytest.mark.parametrize("tariff_id,code", payment_data[-1:])
    async def test_add_payment_correct_data(
        self, async_client, user_login, tariff_id, code
    ):
        payment_url: str = app.url_path_for(
            config.PAYMENT_ADD, tariff_id=tariff_id
        )
        response = await async_client.post(payment_url)
        assert response.status_code == code
        assert parse.quote(conftest.USER_EMAIL) in response.content.decode()

    async def get_payments(self, session):
        stmt = sa.select(Payment)
        result = await session.execute(stmt)
        payments = result.scalars().fetchall()
        return len(payments)

    async def test_get_payments_by_admin(
        self, get_session, async_client, superuser_login
    ):
        response = await async_client.get(
            self.payments_get,
        )
        row = response.content.decode()
        payments = json.loads(row)

        assert len(payments) == await self.get_payments(get_session)

    async def test_get_payments_by_user(
        self, get_session, async_client, user_login
    ):
        response = await async_client.get(
            self.payments_get,
        )
        row = response.content.decode()
        payments = json.loads(row)

        assert len(payments) == await self.get_payments(get_session) - 1
