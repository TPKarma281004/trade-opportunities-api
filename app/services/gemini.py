import json
import logging
import httpx
from ..config import settings

log = logging.getLogger(__name__)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


PROMPT_TEMPLATE = """You are a market analyst. Using the news snippets below, write a concise
trade-opportunity briefing for the {sector} sector in India.

Return clean Markdown with these H2 sections in order:
## Market Overview
## Key Trends
## Top Companies
## Trade Opportunities
## Risks
## Outlook

Keep each section short (3-6 bullet points or 2-3 sentences). Be specific, cite figures
when present in the snippets, and avoid generic filler.

News snippets:
{snippets_block}
"""


def _build_snippets_block(snippets: list[dict]) -> str:
    lines = []
    for i, s in enumerate(snippets, 1):
        lines.append(f"[{i}] {s.get('title','')}\n    {s.get('snippet','')}\n    url: {s.get('url','')}")
    return "\n".join(lines) if lines else "(no snippets returned by search)"


async def analyze_with_gemini(sector: str, snippets: list[dict]) -> str:
    """Call Gemini and return the markdown body. Raises httpx errors on transport issues."""
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY not configured")

    prompt = PROMPT_TEMPLATE.format(sector=sector, snippets_block=_build_snippets_block(snippets))
    url = GEMINI_URL.format(model=settings.gemini_model)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 1200},
    }
    headers = {"Content-Type": "application/json", "x-goog-api-key": settings.gemini_api_key}

    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        resp = await client.post(url, headers=headers, content=json.dumps(payload))
        resp.raise_for_status()
        data = resp.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError) as e:
        log.error("unexpected gemini payload: %s", data)
        raise RuntimeError("Malformed response from Gemini") from e
