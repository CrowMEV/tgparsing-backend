import re

import fastapi as fa
from pydantic import BaseModel, validator


class WsCreateBotSchema(BaseModel):
    api_id: int
    api_hash: str
    phone_number: str

    @validator("phone_number")
    def check_phone(cls, phone):  # pylint: disable=E0213
        pattern = r"^\+7[0-9]{10}$"
        if not re.match(pattern, phone):
            raise fa.HTTPException(
                status_code=fa.status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Неверный номер телефона",
            )
        return phone
