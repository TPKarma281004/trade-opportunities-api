import logging
from typing import Any
from ddgs import DDGS

log = logging.getLogger(__name__)


def fetch_news_snippets(sector: str, limit: int = 8) -> list[dict[str, Any]]:
    """Pull recent India-market news snippets for the given sector via DuckDuckGo."""
    query = f"{sector} sector India market news trade opportunities 2025"
    raw_hits: list[dict[str, Any]] = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, region="in-en", safesearch="moderate", max_results=limit):
                raw_hits.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href") or r.get("url", ""),
                })
    except Exception as e:
        log.warning("ddg search failed: %s", e)
    return raw_hits
