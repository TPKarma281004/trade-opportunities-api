import time
from collections import defaultdict, deque
from fastapi import HTTPException, status, Depends
from .auth import require_api_key
from .config import settings

_hits: dict[str, deque] = defaultdict(deque)

WINDOW_SECONDS = 60


def _prune(key: str, now: float):
    bucket = _hits[key]
    while bucket and now - bucket[0] > WINDOW_SECONDS:
        bucket.popleft()


async def rate_limiter(api_key: str = Depends(require_api_key)):
    """Sliding-window in-memory rate limiter, keyed by API key."""
    now = time.time()
    _prune(api_key, now)
    bucket = _hits[api_key]
    if len(bucket) >= settings.rate_limit_per_minute:
        retry_after = int(WINDOW_SECONDS - (now - bucket[0])) + 1
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {retry_after}s.",
            headers={"Retry-After": str(retry_after)},
        )
    bucket.append(now)
    return api_key
