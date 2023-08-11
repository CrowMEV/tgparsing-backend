import hashlib
from urllib import parse

from settings import config


def calc_signature(*args) -> str:
    return hashlib.md5(":".join(str(arg) for arg in args).encode()).hexdigest()


def generate_payment_link(
    data: dict,
) -> str:
    """URL for redirection of the customer to the service."""
    rk_login = config.RK_LOGIN
    rk_password_1 = config.rk_password_1
    payment_url = config.RK_PAYMENT_URL
    amount = data["amount"]
    inv_id = data["inv_id"]
    email = data["email"]
    signature = calc_signature(rk_login, amount, inv_id, rk_password_1)
    payment_data = {
        "MerchantLogin": rk_login,
        "OutSum": amount,
        "InvId": inv_id,
        "Email": email,
        "SignatureValue": signature,
    }
    if config.RK_ISTEST:
        payment_data.update(
            {
                "IsTest": config.RK_ISTEST,
                "Pass1": rk_password_1,
            }
        )
    return f"{payment_url}?{parse.urlencode(payment_data)}"
