from fastapi import Request
import uuid


def get_or_set_session_id(request: Request) -> str:
    return request.session.setdefault("session_id", str(uuid.uuid4()))
