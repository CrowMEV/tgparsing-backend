from typing import List

import fastapi as fa
from services.role.schemas import RoleNameChoice
from services.user.dependencies import get_current_user
from services.user.models import User


class RoleChecker:
    def __init__(self, allowed_roles: List[RoleNameChoice]):
        self.allowed_roles = [RoleNameChoice(role) for role in allowed_roles]

    def __call__(self, user: User = fa.Depends(get_current_user)):
        if user.role.name not in self.allowed_roles:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_403_FORBIDDEN,
                detail="You have not a permission to perform this action.",
            )


class CheckParserOptions:
    def __init__(self, parser_type: str):
        self.parser_type = parser_type
        self.tariff_options = {
            "parsers_per_day": "Превышен лимит дневных парсеров",
            "simultaneous_parsing": "Превышен лимит одновременных парсеров",
        }

    def __call__(self, user: User = fa.Depends(get_current_user)):
        subscribe = user.subscribe
        if not subscribe:
            raise fa.HTTPException(status_code=403, detail="Тариф отсутствует")
        parser_type_value = subscribe.tariff_options.get(
            self.parser_type, False
        )
        if not isinstance(parser_type_value, bool) or not parser_type_value:
            raise fa.HTTPException(
                status_code=403, detail="Данный тип парсера запрещен"
            )
        for option_key, error_msg in self.tariff_options.items():
            option_value = subscribe.tariff_options.get(option_key, 0)
            if not isinstance(option_value, int) or option_value < 1:
                raise fa.HTTPException(status_code=400, detail=error_msg)
