import fastapi as fa
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket
from pyrogram import Client
from sqlalchemy.ext.asyncio import AsyncSession

import services.telegram.account.db_handlers as db_hand
from database.db_async import get_async_session


ws_router = fa.APIRouter()


@ws_router.websocket("/auth")
async def auth_account(
    api_id: int,
    api_hash: str,
    phone_number: str,
    websocket: WebSocket, session: AsyncSession = fa.Depends(get_async_session)
):
    account = await db_hand.get_tgaccount_by_api_id(session, api_id)
    if account:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Аккаунт с таким api id уже существует",
        )
    client = Client(
        "memory",
        api_id=api_id,
        api_hash=api_hash,
        phone_number=phone_number,
        in_memory=True,
    )

    await client.connect()
    await client.send_code(client.phone_number)
    await websocket.accept()
    phone_code = await websocket.receive_text()
    await websocket.close()
    client.phone_code = phone_code
    await client.authorize()
    session_string = await client.export_session_string()
    data = {
        "api_id": api_id,
        "api_hash": api_hash,
        "phone_number": phone_number,
        "session_string": session_string,
    }
    await client.disconnect()
    await db_hand.create_tgaccount(session, data)
    return JSONResponse(
        status_code=fa.status.HTTP_201_CREATED,
        content={"detail": "Успешно"},
    )
