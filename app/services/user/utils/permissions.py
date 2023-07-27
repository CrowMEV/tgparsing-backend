from fastapi import Depends, HTTPException, status
from services.role.schemas import ActionChoice
from services.user.dependencies import get_current_user


async def is_superuser(user=Depends(get_current_user)) -> None:
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Запрещено",
        )


async def is_admin(user=Depends(get_current_user)) -> None:
    if not user.role.name.value == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Запрещено",
        )


async def payment_read(user=Depends(get_current_user)) -> None:
    if user.is_superuser:
        return
    pay_act = user.role.payment_action
    read = ActionChoice("read")
    if not pay_act or read not in pay_act:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Запрещено",
        )


async def user_read(user=Depends(get_current_user)) -> None:
    if user.is_superuser or user.role.name.value == "admin":
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Запрещено",
    )
