"""
Methods for calling parsing from other server
Not ready
"""


def start_parser_by_subscribes(
    chat: str, api_id: int, api_hash: str, session_string: str
) -> list:
    chat_members = [chat, api_id, api_hash, session_string]
    return chat_members


def info_chat(
    chat: str, api_id: int, api_hash: str, session_string: str
) -> dict:
    info = {
        "chat": chat,
        "api_id": api_id,
        "api_hash": api_hash,
        "session_string": session_string,
    }
    return info
