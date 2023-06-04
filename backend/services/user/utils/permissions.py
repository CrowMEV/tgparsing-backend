from fastapi import Depends, HTTPException, status

from services.user.utils.fastapiusers import fastapi_users


async def is_superuser(user=Depends(fastapi_users.current_user())):
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
