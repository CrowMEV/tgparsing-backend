from datetime import datetime

from dateutil.relativedelta import relativedelta


def get_end_date_of_subscribe(period: str) -> datetime:
    quantity, unit = period.split()
    data = {unit: int(quantity)}
    return datetime.utcnow() + relativedelta(**data)  # type: ignore
