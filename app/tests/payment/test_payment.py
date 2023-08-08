import json

import pytest
import sqlalchemy as sa
from server import app
from services.payment.models import Payment
from settings import config


class TestPayment:
    payments_get: str = app.url_path_for(config.PAYMENTS_GET)

    payment_data = [
        # wrong data
        (100, "someone", 422),
        ("12ad", "addpayment", 422),
        # correct data
        (1000, "admin@gmail.com", 200),
    ]

    @pytest.mark.parametrize("amount,email,code", payment_data[:-1])
    async def test_add_payment_wrong_data(
        self, async_client, user_login, amount, email, code
    ):
        payment_url: str = app.url_path_for(
            config.PAYMENT_ADD,
        )
        response = await async_client.post(
            payment_url, data={"amount": amount, "email": email}
        )
        assert response.status_code == code

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
