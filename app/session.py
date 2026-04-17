import time
from collections import defaultdict

_sessions: dict[str, dict] = defaultdict(lambda: {"count": 0, "last_sector": None, "last_at": None})


def record_usage(api_key: str, sector: str):
    """Track per-key usage in memory. TODO: swap in Redis for prod rate limit + session store."""
    s = _sessions[api_key]
    s["count"] += 1
    s["last_sector"] = sector
    s["last_at"] = time.time()
    return s


def get_usage(api_key: str):
    return _sessions.get(api_key, {"count": 0, "last_sector": None, "last_at": None})
