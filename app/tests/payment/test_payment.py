import json
from datetime import datetime

import pytest
import pytz
import sqlalchemy as sa
from server import app
from services.payment.models import Payment
from settings import config


class TestPayment:
    payments_get: str = app.url_path_for(config.PAYMENTS_GET)
    payment_url: str = app.url_path_for(config.PAYMENT_ADD)
    utc_datetime = (
        datetime.utcnow()
        .astimezone(pytz.timezone("UTC"))
        .replace(microsecond=0)
    )

    payment_data = [
        # Wrong headers
        (
            100,
            "someone",
            {"X-Datetime": f"{utc_datetime}"},
            400,
        ),
        # wrong data
        (
            100,
            "someone",
            {"X-Datetime": f"{utc_datetime.strftime('%Y-%m-%dT%H:%M:%S%z')}"},
            422,
        ),
        (
            "12ad",
            "addpayment",
            {"X-Datetime": f"{utc_datetime.strftime('%Y-%m-%dT%H:%M:%S%z')}"},
            422,
        ),
        # correct data
        (1000, "admin@gmail.com", 200),
    ]

    @pytest.mark.parametrize("amount,email,headers,code", payment_data[:-1])
    async def test_add_payment_wrong_data(
        self, async_client, user_login, amount, email, headers, code
    ):
        response = await async_client.post(
            self.payment_url,
            data={"amount": amount, "email": email},
            headers=headers,
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
