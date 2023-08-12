import hashlib
from datetime import datetime, tzinfo
from urllib import parse

import pytz
from pydantic.types import Decimal
from settings import config


def calc_signature(*args) -> str:
    return hashlib.md5(":".join(str(arg) for arg in args).encode()).hexdigest()


def generate_payment_link(
    ticket_id: int,
    amount: Decimal,
    email: str,
    timezone: str,
) -> str:
    """URL for redirection of the customer to the service."""
    tz_info: tzinfo = pytz.timezone(timezone)
    utc_datetime = datetime.utcnow().replace(tzinfo=pytz.utc)
    local_datetime = utc_datetime.astimezone(tz_info)
    expiration_date = (local_datetime + config.rk_ticket_life).strftime(
        "%Y-%m-%dT%H:%M:%S.%f%z"
    )
    payment_url = config.RK_PAYMENT_URL
    signature = calc_signature(
        config.RK_LOGIN, amount, ticket_id, config.rk_password_1
    )
    # redis_client
    payment_data = {
        "MerchantLogin": config.RK_LOGIN,
        "OutSum": amount,
        "InvId": ticket_id,
        "Email": email,
        "SignatureValue": signature,
        "ExpirationDate": expiration_date,
    }
    if config.RK_ISTEST:
        payment_data.update(
            {
                "IsTest": config.RK_ISTEST,
                "Pass1": config.rk_password_1,
            }
        )
    return f"{payment_url}?{parse.urlencode(payment_data)}"
