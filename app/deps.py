from fastapi import Header, HTTPException, status

from app.config import settings


def require_write_key(x_api_key: str | None = Header(None, alias="X-API-Key")) -> None:
    """Optional API key for mutating routes. Disabled when `settings.api_key` is unset."""
    expected = settings.api_key
    if not expected:
        return
    if x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid X-API-Key header.",
        )
