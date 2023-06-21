from fastapi import Depends, HTTPException, status

from services.user.dependencies import get_current_user


async def is_superuser(user=Depends(get_current_user)) -> None:
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


async def payment_read(user=Depends(get_current_user)) -> None:
    if user.is_superuser:
        return
    pay_act = user.role.payment_action
    if not pay_act or "READ" not in pay_act:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


async def user_read(user=Depends(get_current_user)) -> None:
    if user.is_superuser or user.role.name.name == "ADMIN":
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
