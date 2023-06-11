from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from services.telegram.models import TgAccount


async def get_all_tgaccounts(session: Session):
    return session.query(TgAccount).all()


async def get_tgaccounts(
        session: Session,
        in_work: bool = None,
        is_blocked: bool = None,
        by_geo: bool = None
) -> Sequence[TgAccount]:
    if not in_work and not is_blocked and not by_geo:
        return session.query(TgAccount).filter(
            TgAccount.in_work == False,
            TgAccount.is_blocked == False,
            TgAccount.by_geo == False
        ).all()
    elif in_work and is_blocked and by_geo:
        return session.query(TgAccount).filter(
            TgAccount.in_work == True,
            TgAccount.is_blocked == True,
            TgAccount.by_geo == True
        ).all()
    elif not in_work and is_blocked and by_geo:
        return session.query(TgAccount).filter(
            TgAccount.in_work == False,
            TgAccount.is_blocked == True,
            TgAccount.by_geo == True
        ).all()
    elif not in_work and not is_blocked and by_geo:
        return session.query(TgAccount).filter(
            TgAccount.in_work == False,
            TgAccount.is_blocked == False,
            TgAccount.by_geo == True
        ).all()
    elif not in_work and is_blocked and not by_geo:
        return session.query(TgAccount).filter(
            TgAccount.in_work == False,
            TgAccount.is_blocked == True,
            TgAccount.by_geo == False
        ).all()
    elif in_work and not is_blocked and not by_geo:
        return session.query(TgAccount).filter(
            TgAccount.in_work == True,
            TgAccount.is_blocked == False,
            TgAccount.by_geo == False
        ).all()
    return session.query(TgAccount).all()


async def create_tgaccount(
    session: Session, api_id: int, api_hash: str, session_string: str
) -> TgAccount:
    new_account = TgAccount(
        api_id = api_id,
        api_hash = api_hash,
        session_string = session_string
    )
    # TODO Сделать запрос к api ботов к методу проверок при создании акка
    session.add(new_account)
    session.commit()
    session.refresh(new_account)
    return new_account


async def update_inwork_tgaccount(
        session: Session,
        id_account: int,
        in_work: bool
) -> TgAccount:
    selected_account = session.query(TgAccount).filter(
        TgAccount.id == id_account
    ).first()
    if selected_account:
        selected_account.in_work = in_work
        session.commit()
        session.refresh(selected_account)
    else: return {{'message': 'Неверно указн id аккаунта =('}}
    return selected_account


async def update_isblocked_tgaccount(
        session: Session,
        id_account: int,
        is_blocked: bool
) -> TgAccount:
    selected_account = session.query(TgAccount).filter(
        TgAccount.id == id_account
    ).first()
    if selected_account:
        selected_account.is_blocked = is_blocked
        session.commit()
        session.refresh(selected_account)
    else: return {{'message': 'Неверно указн id аккаунта =('}}
    return selected_account


async def update_bygeo_tgaccount(
        session: Session,
        id_account: int,
        by_geo: bool
) -> TgAccount:
    selected_account = session.query(TgAccount).filter(
        TgAccount.id == id_account
    ).first()
    if selected_account:
        selected_account.by_geo = by_geo
        session.commit()
        session.refresh(selected_account)
    else: return {{'message': 'Неверно указн id аккаунта =('}}
    return selected_account


async def update_sessionstring_tgaccount(
        session: Session,
        id_account: int,
        session_string: str
) -> TgAccount:
    selected_account = session.query(TgAccount).filter(
        TgAccount.id == id_account
    ).first()
    if selected_account:
        selected_account.session_string = session_string
        session.commit()
        session.refresh(selected_account)
    else: return {{'message': 'Неверно указн id аккаунта =('}}
    return selected_account


async def delete_tgaccount(
        session: Session,
        id_account: int
):
    selected_account = session.query(TgAccount).filter(
        TgAccount.id == id_account
    ).first()
    if selected_account:
        session.delete(selected_account)
        session.commit()
    else: return 'Неверно указн id аккаунта =('
