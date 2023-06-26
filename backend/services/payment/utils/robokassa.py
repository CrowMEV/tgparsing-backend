import hashlib
from urllib import parse
from settings import config

from services.payment.schemas import PaymentCreate


def calculate_signature(*args) -> str:
    """Create signature MD5."""
    return hashlib.md5(":".join(str(arg) for arg in args).encode()).hexdigest()


def generate_payment_link(
    inv_id: int,
    payment_data: PaymentCreate,
) -> str:
    """URL for redirection of the customer to the service."""
    check_login = config.RK_CHECK_LOGIN
    check_pass = config.RK_CHECK_PASS_1ST
    payment_url = config.RK_PAYMENT_URL
    tax_system = config.RK_TAX_SYSTEM
    tax = config.RK_TAX
    order_name = config.RK_REPLENISHMENT_NAME
    quantity = 1

    receipt = {
        "sno": tax_system,
        "items": [
            {
                "name": order_name,
                "quantity": quantity,
                "sum": float(payment_data.amount),
                "tax": tax,
            }
        ],
    }
    signature = calculate_signature(
        check_login, payment_data.amount, inv_id, receipt, check_pass
    )
    data = {
        "MerchantLogin": check_login,
        "OutSum": payment_data.amount,
        "InvId": inv_id,
        "Email": payment_data.email or "",
        "Receipt": receipt,
        "SignatureValue": signature,
    }
    return f"{payment_url}?{parse.urlencode(data)}"
