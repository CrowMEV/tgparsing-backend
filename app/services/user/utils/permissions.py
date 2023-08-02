from typing import List

import fastapi as fa
from services.user.dependencies import get_current_user
from services.user.models import User


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = fa.Depends(get_current_user)):
        if user.role.name.value not in self.allowed_roles:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_403_FORBIDDEN,
                detail="You have not a permission to perform this action.",
            )
