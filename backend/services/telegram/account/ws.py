import fastapi as fa
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket
from pydantic import ValidationError
from pyrogram import Client
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import WebSocketException

import services.telegram.account.db_handlers as db_hand
import services.telegram.account.schemas as tg_schemas
from database.db_async import get_async_session

ws_router = fa.APIRouter()


@ws_router.websocket("/auth")
async def auth_account(
    websocket: WebSocket, session: AsyncSession = fa.Depends(get_async_session)
):
    try:
        auth_data = tg_schemas.TgAccountCreate(**websocket.query_params._dict)
    except ValidationError as exc:
        raise WebSocketException(1003, str(exc))
    account = await db_hand.get_tgaccount_by_api_id(session, auth_data.api_id)
    if account:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Аккаунт с таким api id уже существует",
        )
    client = Client(
        "memory",
        api_id=auth_data.api_id,
        api_hash=auth_data.api_hash,
        phone_number=auth_data.phone_number,
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
    data = auth_data.dict()
    data.update(
        {
            "session_string": session_string,
        }
    )
    await client.disconnect()
    await db_hand.create_tgaccount(session, data)
    return JSONResponse(
        status_code=fa.status.HTTP_201_CREATED,
        content={"detail": "Успешно"},
    )
