# India Sector Trade Opportunities API

A small FastAPI service that takes an Indian market sector (e.g. `pharma`, `renewable energy`,
`fintech`) and returns a trade-opportunity briefing in Markdown. It pulls recent news snippets
from DuckDuckGo and asks Google Gemini to summarize them into a structured report.

## Stack
- FastAPI + Uvicorn
- Pydantic v2 for input validation
- DuckDuckGo Search (`ddgs`) for news retrieval — no API key needed
- Google Gemini (`gemini-1.5-flash`) for analysis
- In-memory rate limiting + session usage tracking
- Guest auth via `X-API-Key` header

## Setup

```bash
python -m venv .venv
source .venv/bin/activate    # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set GEMINI_API_KEY
bash run.sh
```

Open http://localhost:8000/docs for the Swagger UI.

## Environment variables

| Var | Default | Purpose |
|-----|---------|---------|
| `GEMINI_API_KEY` | _(required)_ | From https://aistudio.google.com/app/apikey |
| `API_KEY` | `guest-demo-key` | Value clients must send in `X-API-Key` |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Override if needed |
| `RATE_LIMIT_PER_MINUTE` | `5` | Per-key request cap |
| `SEARCH_RESULTS` | `8` | Number of news snippets to fetch |
| `REQUEST_TIMEOUT` | `30` | Gemini HTTP timeout (seconds) |

## Endpoints

### `GET /analyze/{sector}`
Returns a JSON envelope with a markdown report.

```bash
curl -H "X-API-Key: guest-demo-key" \
     http://localhost:8000/analyze/pharma
```

Add `?format=md` to receive raw `text/markdown` instead of JSON.

### `GET /usage`
Returns the calling key's session usage.

### `GET /`
Health check.

## Error codes
- `401` missing/invalid API key
- `422` invalid sector name
- `429` rate limit exceeded (includes `Retry-After`)
- `502` upstream Gemini or search failure

## Notes
Rate limiting and session tracking are intentionally in-memory for simplicity. For production
you'd swap them for Redis (there's a `TODO` in `rate_limit.py`).
