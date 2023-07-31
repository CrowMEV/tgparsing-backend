from fastapi import Depends, HTTPException, status
from services.role.schemas import ActionChoice
from services.user.dependencies import get_current_user


async def is_superuser(user=Depends(get_current_user)) -> None:
    if not user.role.name.value in ["superuser"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Запрещено",
        )


async def is_admin(user=Depends(get_current_user)) -> None:
    if not user.role.name.value in ["admin", "superuser"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Запрещено",
        )


async def is_user(user=Depends(get_current_user)) -> None:
    if not user.role.name.value == "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Запрещено",
        )


async def payment_read(user=Depends(get_current_user)) -> None:
    if user.role.name.value == "superuser":
        return
    pay_act = user.role.payment_action
    read = ActionChoice("read")
    if not pay_act or read not in pay_act:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Запрещено",
        )


async def user_read(user=Depends(get_current_user)) -> None:
    if user.role.name.value in ["admin", "superuser"]:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Запрещено",
    )
