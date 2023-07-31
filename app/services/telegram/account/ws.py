import fastapi as fa
import services.telegram.account.db_handlers as db_hand
from database.db_async import get_async_session
from fastapi.websockets import WebSocket
from pyrogram import Client
from pyrogram.errors import ApiIdInvalid, PhoneCodeExpired, PhoneCodeInvalid
from sqlalchemy.ext.asyncio import AsyncSession


ws_router = fa.APIRouter()


@ws_router.websocket("/auth")
async def auth_account(
    api_id: int,
    api_hash: str,
    phone_number: str,
    websocket: WebSocket,
    session: AsyncSession = fa.Depends(get_async_session),
):
    await websocket.accept()
    account = await db_hand.get_tgaccount_by_api_id(session, api_id)
    if account:
        raise fa.WebSocketException(
            code=fa.status.WS_1003_UNSUPPORTED_DATA,
            reason="Аккаунт с таким api id уже существует",
        )
    try:
        client = Client(
            "memory",
            api_id=api_id,
            api_hash=api_hash,
            phone_number=phone_number,
            in_memory=True,
        )
        await client.connect()
        code_response = await client.send_code(client.phone_number)
        phone_code_hash = code_response.phone_code_hash
    except ApiIdInvalid as exc:
        raise fa.WebSocketException(
            code=fa.status.WS_1003_UNSUPPORTED_DATA,
            reason=exc.MESSAGE,
        )
    await websocket.send_text("Enter the code")
    phone_code = await websocket.receive_text()
    client.phone_code = phone_code
    try:
        await client.sign_in(phone_number, phone_code_hash, phone_code)
    except PhoneCodeInvalid as exc:
        raise fa.WebSocketException(
            code=fa.status.WS_1003_UNSUPPORTED_DATA,
            reason=exc.MESSAGE,
        )
    except PhoneCodeExpired:
        raise fa.WebSocketException(  # pylint: disable=W0707
            code=fa.status.WS_1003_UNSUPPORTED_DATA,
            reason="The phone does not belong to this account",
        )
    session_string = await client.export_session_string()
    data = {
        "api_id": api_id,
        "api_hash": api_hash,
        "phone_number": phone_number,
        "session_string": session_string,
    }
    await client.disconnect()
    await db_hand.create_tgaccount(session, data)
    await websocket.close(reason="Account created successfully")
