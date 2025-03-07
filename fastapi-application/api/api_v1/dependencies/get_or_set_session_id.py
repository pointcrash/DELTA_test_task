from fastapi import Request
import uuid


def get_or_set_session_id(request: Request) -> str:
    """Get or set a unique session ID from the request session."""
    return request.session.setdefault("session_id", str(uuid.uuid4()))
