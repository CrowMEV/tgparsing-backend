import decimal
import hashlib
from urllib import parse
from settings import config


def calculate_signature(*args) -> str:
    """Create signature MD5."""
    return hashlib.md5(":".join(str(arg) for arg in args).encode()).hexdigest()


def generate_payment_link(
    amount: decimal.Decimal,
    inv_id: int,
    email: str,
) -> str:
    """URL for redirection of the customer to the service."""
    merchant_login = config.RK_CHECK_LOGIN
    merchant_password_1 = config.RK_CHECK_PASS
    payment_url = config.RK_PAYMENT_URL
    signature = calculate_signature(
        merchant_login, amount, inv_id, merchant_password_1
    )
    data = {
        "MerchantLogin": merchant_login,
        "OutSum": amount,
        "InvId": inv_id,
        "Email": email,
        "SignatureValue": signature,
    }
    return f"{payment_url}?{parse.urlencode(data)}"
