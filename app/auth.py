from fastapi import Header, HTTPException, status
from .config import settings


async def require_api_key(x_api_key: str = Header(default=None, alias="X-API-Key")):
    """Guest-style API key check. Reads X-API-Key header and matches it against the configured key."""
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
        )
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return x_api_key
