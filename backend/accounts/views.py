import random

import sqlalchemy as sa
from fastapi import Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
from database.models.account_model import TelegramAccount as Acc
from accounts.schemas import AccountCreate, AccountUpdate
from starlette import status
from fastapi.responses import JSONResponse
from accounts.utils.humanhash import humanize


async def get_account(
    account_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(get_async_session),
):
    query = sa.select(Acc.api_id, Acc.api_hash, Acc.session).filter(
        Acc.id == account_id
    )
    result = await session.execute(query)
    result = result.fetchone()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Account with id={account_id} does not exist",
        )
    data = {
        "api_id": result.api_id,
        "api_hash": result.api_hash,
        "session": result.session,
    }
    return {
        "data": data,
    }


async def get_account_by_params(
    is_blocked: bool = False,
    by_geo: bool = False,
    session: AsyncSession = Depends(get_async_session),
):
    query = (
        sa.select(Acc.api_id, Acc.api_hash, Acc.session)
        .filter(Acc.is_blocked == is_blocked)
        .filter(Acc.by_geo == by_geo)
    )
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No matches by the specified parameters",
        )
    account = random.choice(result)

    data = {
        "api_id": account.api_id,
        "api_hash": account.api_hash,
        "session": account.session,
    }
    return {
        "data": data,
    }


async def add_account(
    new_account: AccountCreate,
    session: AsyncSession = Depends(get_async_session),
):
    data = new_account.dict()
    existing_role = await session.execute(
        sa.select(Acc).filter(Acc.api_id == data["api_id"])
    )
    if existing_role.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Account with api_id={data['api_id']} already exists",
        )
    stmt = sa.insert(Acc).values(data)

    await session.execute(stmt)
    await session.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "msg": f"Account {humanize(data['api_hash'])} was added",
        },
    )


async def update_account(
    new_account: AccountUpdate,
    account_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(get_async_session),
):
    data = new_account.dict()
    actual_data = {
        key: value for key, value in data.items() if value is not None
    }
    stmt = sa.update(Acc).where(Acc.id == account_id).values(actual_data)
    await session.execute(stmt)
    await session.commit()
    return {
        "msg": "Account successfully updated",
    }


async def delete_account(
    account_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(get_async_session),
):
    query = sa.select(Acc).filter(Acc.id == account_id)
    account = await session.execute(query)
    account = account.fetchone()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Account with id={account_id} does not exist",
        )
    await session.delete(account[0])
    await session.commit()
    return {
        "msg": "Account successfully deleted",
    }
