import time
import hmac
import hashlib
from aiohttp import web
from config import settings

COOKIE_NAME = "admin_session"
SESSION_DURATION = 7 * 24 * 3600  # 7 дней

def create_session_token(username: str) -> str:
    timestamp = str(int(time.time()))
    payload = f"{username}:{timestamp}"
    signature = hmac.new(
        settings.SESSION_SECRET.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload}:{signature}"

def verify_session_token(token: str | None) -> str | None:
    if not token:
        return None

    try:
        parts = token.split(":")
        if len(parts) != 3:
            return None

        username, timestamp_str, signature = parts
        timestamp = int(timestamp_str)

        # Проверка срока жизни
        if time.time() - timestamp > SESSION_DURATION:
            return None

        payload = f"{username}:{timestamp_str}"
        expected_sig = hmac.new(
            settings.SESSION_SECRET.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        if hmac.compare_digest(signature, expected_sig):
            return username
        return None
    except Exception:
        return None

def is_authenticated(request: web.Request) -> bool:
    token = request.cookies.get(COOKIE_NAME)
    return verify_session_token(token) is not None

def set_session_cookie(response: web.StreamResponse, username: str) -> None:
    token = create_session_token(username)
    response.set_cookie(
        COOKIE_NAME,
        token,
        max_age=SESSION_DURATION,
        httponly=True,
        samesite="Lax",
        path="/",
    )

def clear_session_cookie(response: web.StreamResponse) -> None:
    response.del_cookie(COOKIE_NAME, path="/")
