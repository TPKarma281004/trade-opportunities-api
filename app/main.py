import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import analyze

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
)

app = FastAPI(
    title="India Sector Trade Opportunities API",
    description="A small FastAPI service that analyzes recent market news for an Indian sector "
                "and returns an LLM-generated trade-opportunity briefing.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(analyze.router, tags=["analysis"])


@app.get("/", summary="Health check")
async def root():
    """Basic liveness probe."""
    return {"status": "ok", "service": "trade-opportunities-api"}
