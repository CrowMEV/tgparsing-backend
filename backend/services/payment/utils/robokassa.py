import hashlib
from urllib import parse

from services.payment.schemas import PaymentCreate
from settings import config


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


def check_result_payment(params, strict_check: bool = False) -> bool:
    check_pass = (
        config.RK_CHECK_PASS_2ND if strict_check else config.RK_CHECK_PASS_1ST
    )
    signature = calculate_signature(params.out_sum, params.inv_id, check_pass)
    if signature.lower() == params.signature_value.lower():
        return True
    return False
