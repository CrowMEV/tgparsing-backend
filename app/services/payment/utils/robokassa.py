import hashlib
from urllib import parse

from settings import config


def calculate_signature(*args) -> str:
    return hashlib.md5(":".join(str(arg) for arg in args).encode()).hexdigest()


def generate_payment_link(
    data: dict,
) -> str:
    """URL for redirection of the customer to the service."""
    check_login = config.RK_CHECK_LOGIN
    pass_1 = config.RK_CHECK_PASS_1ST
    payment_url = config.RK_PAYMENT_URL
    amount = data["amount"]
    inv_id = data["inv_id"]
    email = data["email"]
    signature = calculate_signature(check_login, amount, inv_id, pass_1)
    payment_data = {
        "MerchantLogin": check_login,
        "OutSum": amount,
        "InvId": inv_id,
        "Email": email,
        "SignatureValue": signature,
    }
    return parse.urljoin(payment_url, parse.urlencode(payment_data))
