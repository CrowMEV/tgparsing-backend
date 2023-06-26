import random
from urllib import parse
from urllib.parse import parse_qs, urlparse

import pytest
import sqlalchemy as sa

from server import app
from services.payment.models import Payment
from services.payment.utils.robokassa import calculate_signature
from settings import config
from tests import conftest


class TestPayment:
    payment_url: str = app.url_path_for(config.PAYMENT_ADD)
    payment_chk: str = app.url_path_for(config.PAYMENT_CHK)
    payment_upd: str = app.url_path_for(config.PAYMENT_UPD)

    payment_data = [
        # wrong data
        (0, 422),
        (1.123, 422),
        # correct data
        (1, 200),
    ]

    @pytest.mark.parametrize("amount,code", payment_data[:-1])
    async def test_add_payment_wrong_data(
        self, async_client, user_login, amount, code
    ):
        response = await async_client.post(
            self.payment_url,
            json={"amount": amount},
        )

        assert response.status_code == code

    @pytest.mark.parametrize("amount,code", payment_data[-1:])
    async def test_add_payment_correct_data(
        self, async_client, user_login, amount, code
    ):
        response = await async_client.post(
            self.payment_url,
            json={"amount": amount},
        )

        assert response.status_code == code
        assert parse.quote(conftest.USER_EMAIL) in response.content.decode()

    amount = random.uniform(1, 100000)
    inv_id = random.randint(1, 100000)
    correct_signature = calculate_signature(
        amount, inv_id, config.RK_CHECK_PASS_2ND
    )
    wrong_signature = calculate_signature(
        amount, inv_id, config.RK_CHECK_PASS_2ND
    )[:-1]
    url_data = [
        # wrong data
        (amount, inv_id, wrong_signature, config.RK_BAD_SIGNATURE),
        # correct data
        (amount, inv_id, correct_signature, f"OK{inv_id}"),
    ]

    @pytest.mark.parametrize("amount, inv_id, signature, msg", url_data)
    async def test_check_response_payment(
        self, async_client, amount, inv_id, signature, msg
    ):
        params = {
            "OutSum": amount,
            "InvId": inv_id,
            "SignatureValue": signature,
        }
        response = await async_client.get(self.payment_chk, params=params)

        assert response.status_code == 200
        assert msg in response.content.decode()

    async def test_confirm_payment(self, session, async_client):
        amount = round(random.uniform(1, 100000), 2)

        url = await async_client.post(
            self.payment_url,
            json={"amount": amount},
        )

        parsed_url = urlparse(url.content.decode())
        query_params = parse_qs(parsed_url.query)
        inv_id = int(query_params.get("InvId")[0])
        signature = calculate_signature(
            amount, inv_id, config.RK_CHECK_PASS_1ST
        )

        params = {
            "OutSum": amount,
            "InvId": inv_id,
            "SignatureValue": signature,
        }
        await async_client.get(self.payment_upd, params=params)

        stmt = sa.select(Payment).where(Payment.id == inv_id)
        result = await session.execute(stmt)
        payment = result.scalars().first()

        assert payment.status is True
