from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from services.telegram.models import TgAccount


async def get_all_tgaccounts(session: AsyncSession):
    # return await session.query(TgAccount).all()

    stmt = sa.select(TgAccount)
    result = await session.execute(stmt)
    tg_accounts = result.scalars().fetchall()
    return tg_accounts


async def create_tgaccount(
    session: AsyncSession, api_id: int, api_hash: str, session_string: str
) -> TgAccount:
    ins = insert(TgAccount).values(
        api_id=api_id, api_hash=api_hash, session_string=session_string
    ).returning(TgAccount)
    result = await session.execute(ins)
    # await session.commit()
    new_account = result.scalars().first()
    return new_account


# async def get_all_tgaccounts(session: AsyncSession):
#     # return await session.query(TgAccount).all()

#     stmt = sa.select(TgAccount)
#     result = await session.execute(stmt)
#     tg_accounts = result.scalars().fetchall()
#     return tg_accounts


# async def get_tgaccounts(
#         session: AsyncSession,
#         in_work: bool = None,
#         is_blocked: bool = None,
#         by_geo: bool = None
# ) -> Sequence[TgAccount]:
#     if not in_work and not is_blocked and not by_geo:
#         return await session.query(TgAccount).filter(
#             TgAccount.in_work == False,
#             TgAccount.is_blocked == False,
#             TgAccount.by_geo == False
#         ).all()
#     elif in_work and is_blocked and by_geo:
#         return await session.query(TgAccount).filter(
#             TgAccount.in_work == True,
#             TgAccount.is_blocked == True,
#             TgAccount.by_geo == True
#         ).all()
#     elif not in_work and is_blocked and by_geo:
#         return await session.query(TgAccount).filter(
#             TgAccount.in_work == False,
#             TgAccount.is_blocked == True,
#             TgAccount.by_geo == True
#         ).all()
#     elif not in_work and not is_blocked and by_geo:
#         return await session.query(TgAccount).filter(
#             TgAccount.in_work == False,
#             TgAccount.is_blocked == False,
#             TgAccount.by_geo == True
#         ).all()
#     elif not in_work and is_blocked and not by_geo:
#         return await session.query(TgAccount).filter(
#             TgAccount.in_work == False,
#             TgAccount.is_blocked == True,
#             TgAccount.by_geo == False
#         ).all()
#     elif in_work and not is_blocked and not by_geo:
#         return await session.query(TgAccount).filter(
#             TgAccount.in_work == True,
#             TgAccount.is_blocked == False,
#             TgAccount.by_geo == False
#         ).all()
#     return await session.query(TgAccount).all()


# async def create_tgaccount(
#         session: AsyncSession,
#         api_id: int,
#         api_hash: str,
#         session_string: str
# ) -> TgAccount:
#     # s_maker = sessionmaker(bind=session)
#     new_account = {
#         'api_id': api_id,
#         'api_hash': api_hash,
#         'session_strins': session_string
#     }
#     # TODO Сделать запрос к api ботов к методу проверок при создании акка
#     # session.add(new_account)
#     # await session.commit()
#     # await session.refresh(new_account)

#     # stmt = sa.insert(TgAccount).values(new_account).returning(TgAccount)
#     # result = await session.execute(stmt)
#     # acc = result.scalars().first()
#     # await session.commit()

#     new_acc = session.add(
#         TgAccount(
#         api_id = api_id,
#         api_hash = api_hash,
#         session_strins = session_string
#         )
#     )
#     return new_acc


# async def update_inwork_tgaccount(
#         session: AsyncSession,
#         id_account: int,
#         in_work: bool
# ) -> TgAccount:
#     selected_account = session.query(TgAccount).filter(
#         TgAccount.id == id_account
#     ).first()
#     if selected_account:
#         selected_account.in_work = in_work
#         session.commit()
#         session.refresh(selected_account)
#     else: return {{'message': 'Неверно указн id аккаунта =('}}
#     return selected_account


# async def update_isblocked_tgaccount(
#         session: AsyncSession,
#         id_account: int,
#         is_blocked: bool
# ) -> TgAccount:
#     selected_account = session.query(TgAccount).filter(
#         TgAccount.id == id_account
#     ).first()
#     if selected_account:
#         selected_account.is_blocked = is_blocked
#         session.commit()
#         session.refresh(selected_account)
#     else: return {{'message': 'Неверно указн id аккаунта =('}}
#     return selected_account


# async def update_bygeo_tgaccount(
#         session: AsyncSession,
#         id_account: int,
#         by_geo: bool
# ) -> TgAccount:
#     selected_account = session.query(TgAccount).filter(
#         TgAccount.id == id_account
#     ).first()
#     if selected_account:
#         selected_account.byby_geo =by_geo
#         session.commit()
#         session.refresh(selected_account)
#     else: return {{'message': 'Неверно указн id аккаунта =('}}
#     return selected_account


# async def update_sessionstring_tgaccount(
#         session: AsyncSession,
#         id_account: int,
#         session_string: str
# ) -> TgAccount:
#     selected_account = session.query(TgAccount).filter(
#         TgAccount.id == id_account
#     ).first()
#     if selected_account:
#         selected_account.session_string = session_string
#         session.commit()
#         session.refresh(selected_account)
#     else: return {{'message': 'Неверно указн id аккаунта =('}}
#     return selected_account


# async def delete_tgaccount(
#         session: AsyncSession,
#         id_account: int
# ):
#     selected_account = session.query(TgAccount).filter(
#         TgAccount.id == id_account
#     ).first()
#     if selected_account:
#         session.delete(selected_account)
#         session.commit()
#         return {{'message': 'Ok'}}
#     else: return {{'message': 'Неверно указн id аккаунта =('}}
