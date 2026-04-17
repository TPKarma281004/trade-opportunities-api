import logging
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import PlainTextResponse, JSONResponse

from ..rate_limit import rate_limiter
from ..schemas import SectorIn, AnalyzeResponse
from ..services.search import fetch_news_snippets
from ..services.gemini import analyze_with_gemini
from ..report import build_report
from ..session import record_usage, get_usage
from ..config import settings

log = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/analyze/{sector}",
    summary="Analyze a sector and return a trade-opportunity briefing",
    response_model=None,
)
async def analyze_sector(
    sector: str,
    format: str = Query(default="json", pattern="^(json|md)$"),
    api_key: str = Depends(rate_limiter),
):
    """Validate the sector, pull news, ask Gemini, return a markdown briefing."""
    try:
        validated = SectorIn(sector=sector).sector
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    log.info("analyze request sector=%s key=%s...", validated, api_key[:4])
    raw_hits = fetch_news_snippets(validated, limit=settings.search_results)
    sources = [h["url"] for h in raw_hits if h.get("url")]

    try:
        body_md = await analyze_with_gemini(validated, raw_hits)
    except httpx.HTTPStatusError as e:
        log.error("gemini http error: %s", e.response.text)
        raise HTTPException(status_code=502, detail="Upstream Gemini error")
    except (httpx.HTTPError, RuntimeError) as e:
        log.error("gemini failure: %s", e)
        raise HTTPException(status_code=502, detail=f"Gemini analysis failed: {e}")

    report_md, ts = build_report(validated, body_md, sources)
    usage = record_usage(api_key, validated)

    if format == "md":
        return PlainTextResponse(report_md, media_type="text/markdown")

    return AnalyzeResponse(
        sector=validated,
        generated_at=ts,
        report_markdown=report_md,
        sources=sources,
        usage={"requests_this_session": usage["count"], "last_sector": usage["last_sector"]},
    )


@router.get("/usage", summary="Inspect session usage for the calling key")
async def usage(api_key: str = Depends(rate_limiter)):
    return JSONResponse(get_usage(api_key))
