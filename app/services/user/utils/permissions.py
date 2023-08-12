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
